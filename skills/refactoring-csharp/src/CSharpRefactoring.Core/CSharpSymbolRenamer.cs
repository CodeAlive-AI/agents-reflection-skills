using System.ComponentModel;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.FindSymbols;
using Microsoft.CodeAnalysis.MSBuild;
using Microsoft.CodeAnalysis.Rename;
using Microsoft.CodeAnalysis.Text;
using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;

namespace CSharpRefactoring.Core;

public static class CSharpSymbolRenamer
{
    public sealed class RenameResult
    {
        public bool Success { get; init; }
        public string? ErrorCode { get; init; }
        public string? Message { get; init; }
        public string? Mode { get; init; }
        public string? OriginalName { get; init; }
        public string? NewName { get; init; }
        public string? SymbolKind { get; init; }
        public string? SymbolDisplay { get; init; }
        public string? FilePath { get; init; }
        public string? FileMoveFromPath { get; init; }
        public string? FileMoveToPath { get; init; }
        public int StartLine { get; init; }
        public int StartColumn { get; init; }
        public int EndLine { get; init; }
        public int EndColumn { get; init; }
        public bool DryRun { get; init; }
        public int ChangedDocumentCount { get; init; }
        public int TotalTextChanges { get; init; }
        public IReadOnlyList<ChangedDocument> ChangedDocuments { get; init; } = Array.Empty<ChangedDocument>();
    }

    public sealed class RenamePrepareResult
    {
        public bool Success { get; init; }
        public string? ErrorCode { get; init; }
        public string? Message { get; init; }
        public string? Placeholder { get; init; }
        public string? SymbolKind { get; init; }
        public int StartLine { get; init; }
        public int StartColumn { get; init; }
        public int EndLine { get; init; }
        public int EndColumn { get; init; }
    }

    public sealed class ChangedDocument
    {
        public string FilePath { get; init; } = string.Empty;
        public int Changes { get; init; }
    }

    private sealed class RenameCandidate
    {
        public ISymbol Symbol { get; init; } = null!;
        public Document Document { get; init; } = null!;
        public TextSpan RenameSpan { get; init; }
        public string Placeholder { get; init; } = string.Empty;
        public int StartLine { get; init; }
        public int StartColumn { get; init; }
        public int EndLine { get; init; }
        public int EndColumn { get; init; }
    }

    [McpServerToolType]
    public static class Tool
    {
        private static readonly HashSet<SymbolKind> SupportedSymbolKinds =
        [
            SymbolKind.NamedType,
            SymbolKind.Method,
            SymbolKind.Property,
            SymbolKind.Field,
            SymbolKind.Event,
            SymbolKind.Parameter,
            SymbolKind.Local,
            SymbolKind.TypeParameter,
            SymbolKind.Namespace
        ];

        private const int MinTimeoutSeconds = 1;
        private const int MaxTimeoutSeconds = 600;
        private const int DefaultTimeoutSeconds = 30;

        [McpServerTool, Description("Rename a C# symbol in a solution using file, line, and old symbol name.")]
        public static async Task<RenameResult> RenameSymbol(
            [Description("Absolute path to .sln or .slnx file")] string solutionPath,
            [Description("Absolute path to target document inside that solution")] string filePath,
            [Description("1-based line number")] int lineNumber,
            [Description("Expected current symbol name on the selected line")] string oldName,
            [Description("New symbol name")] string newName,
            [Description("When true, do not apply changes, return dry-run diff only")] bool dryRun = false,
            [Description("Rename overloads for method symbols as well")] bool renameOverloads = false,
            [Description("Rename identifiers in string literals too")] bool renameInStrings = false,
            [Description("Rename identifiers in comments too")] bool renameInComments = true,
            [Description("Rename file if symbol is a type")] bool renameFile = true,
            [Description("Override operation timeout in seconds")] int timeoutSeconds = DefaultTimeoutSeconds)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(solutionPath) || !File.Exists(solutionPath))
                {
                    return Error("invalid_solution_path", "solutionPath must be an existing .sln or .slnx file.");
                }

                if (string.IsNullOrWhiteSpace(filePath) || !File.Exists(filePath))
                {
                    return Error("invalid_file_path", "filePath must be an existing file inside the solution.");
                }

                if (!IsSupportedSolutionFile(solutionPath))
                {
                    return Error("invalid_solution_extension", "solutionPath must have .sln or .slnx extension.");
                }

                if (lineNumber < 1)
                {
                    return Error("invalid_line_number", "lineNumber is 1-based and must be >= 1.");
                }

                if (string.IsNullOrWhiteSpace(oldName))
                {
                    return Error("invalid_old_name", "oldName must be provided.");
                }

                if (!IsValidCSharpIdentifier(newName))
                {
                    return Error("invalid_new_name", "newName must be a valid C# identifier.");
                }

                using (CancellationTokenSource cts = CreateCancellationTokenSource(timeoutSeconds))
                {
                    string? solutionDirectory = Path.GetDirectoryName(Path.GetFullPath(solutionPath));
                    string previousCurrentDirectory = Directory.GetCurrentDirectory();
                    try
                    {
                        if (!string.IsNullOrWhiteSpace(solutionDirectory))
                        {
                            Directory.SetCurrentDirectory(solutionDirectory);
                        }

                        using (MSBuildWorkspace workspace = MSBuildWorkspace.Create())
                        {
                            Solution solution = await workspace.OpenSolutionAsync(solutionPath, cancellationToken: cts.Token);
                            if (solution is null)
                            {
                                return Error("workspace_open_failed", "Could not open solution workspace.");
                            }

                            string normalizedFilePath = Path.GetFullPath(filePath);
                            Document? doc = FindDocument(solution, normalizedFilePath);
                            if (doc is null)
                            {
                                return Error("file_not_in_solution", "Could not find file in loaded solution documents.");
                            }

                            (RenameCandidate? candidate, string? errorCode, string? message) =
                                await ResolveRenameCandidateAsync(doc, lineNumber, oldName, cts.Token);

                            if (candidate is null)
                            {
                                return Error(errorCode ?? "invalid_rename_target", message ?? "Cannot determine rename target.");
                            }

                            if (!CanRenameSymbol(candidate.Symbol))
                            {
                                return Error("unsupported_symbol_kind", $"Symbol kind '{candidate.Symbol.Kind}' is not supported for rename.");
                            }

                            if (!IsSourceSymbol(candidate.Symbol))
                            {
                                return Error("symbol_not_in_source", "Can only rename symbols declared in source files.");
                            }

                            string normalizedCurrentName = NormalizeIdentifierText(candidate.Symbol.Name);
                            string normalizedNewName = NormalizeIdentifierText(newName);
                            if (string.Equals(normalizedCurrentName, normalizedNewName, StringComparison.Ordinal))
                            {
                                return Error("same_name", "newName is same as current name.");
                            }

                            string? fileMoveFromPath = null;
                            string? fileMoveToPath = null;
                            (fileMoveFromPath, fileMoveToPath) = GetFileRenamePlan(candidate.Document, candidate.Symbol, newName, renameFile);

                            SymbolRenameOptions renameOptions = new(renameOverloads, renameInStrings, renameInComments, false);

                            Solution renamedSolution = await Renamer.RenameSymbolAsync(
                                solution,
                                candidate.Symbol,
                                renameOptions,
                                newName,
                                cts.Token);

                            List<ChangedDocument> changed = new();
                            foreach (Document oldDoc in solution.Projects.SelectMany(project => project.Documents))
                            {
                                Document? newDoc = renamedSolution.GetDocument(oldDoc.Id);
                                if (newDoc is null)
                                {
                                    continue;
                                }

                                string oldFilePath = oldDoc.FilePath ?? string.Empty;
                                string newFilePath = newDoc.FilePath ?? oldFilePath;
                                bool plannedFileMove = !string.IsNullOrWhiteSpace(fileMoveFromPath)
                                    && !string.IsNullOrWhiteSpace(fileMoveToPath)
                                    && string.Equals(Path.GetFullPath(oldFilePath), Path.GetFullPath(fileMoveFromPath), StringComparison.OrdinalIgnoreCase);
                                if (plannedFileMove)
                                {
                                    newFilePath = fileMoveToPath!;
                                }

                                bool fileMoved = plannedFileMove
                                    || !string.Equals(oldFilePath, newFilePath, StringComparison.OrdinalIgnoreCase);
                                SourceText oldText = await oldDoc.GetTextAsync(cts.Token);
                                SourceText newText = await newDoc.GetTextAsync(cts.Token);
                                int changes = oldText.GetTextChanges(newText).Count();
                                if (!fileMoved && changes <= 0)
                                {
                                    continue;
                                }

                                changed.Add(new ChangedDocument
                                {
                                    FilePath = newFilePath,
                                    Changes = changes
                                });

                                if (fileMoved && string.IsNullOrWhiteSpace(fileMoveFromPath))
                                {
                                    fileMoveFromPath = oldFilePath;
                                    fileMoveToPath = newFilePath;
                                }
                            }

                            if (changed.Count == 0)
                            {
                                return Error("no_changes", "Rename produced no document changes.");
                            }

                            if (!dryRun)
                            {
                                await ApplyRenamedSolutionToDiskAsync(solution, renamedSolution, fileMoveFromPath, fileMoveToPath, cts.Token);
                            }

                            string resultMessage = dryRun
                                ? $"Dry-run: '{candidate.Symbol.Name}' -> '{newName}'. {changed.Count} documents would change."
                                : $"Renamed '{candidate.Symbol.Name}' -> '{newName}'. {changed.Count} documents changed.";

                            if (!string.IsNullOrWhiteSpace(fileMoveFromPath) && !string.IsNullOrWhiteSpace(fileMoveToPath))
                            {
                                resultMessage += $" File moved: '{fileMoveFromPath}' -> '{fileMoveToPath}'.";
                            }

                            RenameResult result = new()
                            {
                                Success = true,
                                Mode = dryRun ? "dry_run" : "applied",
                                OriginalName = candidate.Symbol.Name,
                                NewName = newName,
                                SymbolKind = candidate.Symbol.Kind.ToString(),
                                SymbolDisplay = candidate.Symbol.ToDisplayString(SymbolDisplayFormat.MinimallyQualifiedFormat),
                                FilePath = normalizedFilePath,
                                FileMoveFromPath = fileMoveFromPath,
                                FileMoveToPath = fileMoveToPath,
                                StartLine = candidate.StartLine,
                                StartColumn = candidate.StartColumn,
                                EndLine = candidate.EndLine,
                                EndColumn = candidate.EndColumn,
                                DryRun = dryRun,
                                ChangedDocumentCount = changed.Count,
                                TotalTextChanges = changed.Sum(c => c.Changes),
                                ChangedDocuments = changed,
                                Message = resultMessage
                            };

                            return result;
                        }
                    }
                    finally
                    {
                        Directory.SetCurrentDirectory(previousCurrentDirectory);
                    }
                }
            }
            catch (OperationCanceledException)
            {
                return Error("operation_timeout", "Rename operation timed out.");
            }
            catch (ArgumentException ex)
            {
                return Error("invalid_argument", ex.Message);
            }
            catch (UnauthorizedAccessException ex)
            {
                return Error("access_denied", ex.Message);
            }
            catch (IOException ex)
            {
                return Error("io_error", ex.Message);
            }
            catch (InvalidOperationException ex)
            {
                return Error("invalid_operation", ex.Message);
            }
            catch (Exception ex)
            {
                return Error("unexpected_error", ex.Message);
            }
        }

        [Description("Validate and prepare a rename target in a document position.")]
        private static async Task<RenamePrepareResult> PrepareRenameAtPosition(
            [Description("Absolute path to .sln or .slnx file")] string solutionPath,
            [Description("Absolute path to target document inside that solution")] string filePath,
            [Description("1-based line number")] int line,
            [Description("1-based column number")] int column,
            [Description("Override operation timeout in seconds")] int timeoutSeconds = DefaultTimeoutSeconds)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(solutionPath) || !File.Exists(solutionPath))
                {
                    return ErrorPrepare("invalid_solution_path", "solutionPath must be an existing .sln or .slnx file.");
                }

                if (string.IsNullOrWhiteSpace(filePath) || !File.Exists(filePath))
                {
                    return ErrorPrepare("invalid_file_path", "filePath must be an existing file inside the solution.");
                }

                if (!IsSupportedSolutionFile(solutionPath))
                {
                    return ErrorPrepare("invalid_solution_extension", "solutionPath must have .sln or .slnx extension.");
                }

                if (line < 1 || column < 1)
                {
                    return ErrorPrepare("invalid_position", "line and column are 1-based and must be >= 1.");
                }

                using (CancellationTokenSource cts = CreateCancellationTokenSource(timeoutSeconds))
                {
                    using MSBuildWorkspace workspace = MSBuildWorkspace.Create();
                    Solution solution = await workspace.OpenSolutionAsync(solutionPath, cancellationToken: cts.Token);
                    if (solution is null)
                    {
                        return ErrorPrepare("workspace_open_failed", "Could not open solution workspace.");
                    }

                    string fullFilePath = Path.GetFullPath(filePath);
                    Document? doc = FindDocument(solution, fullFilePath);
                    if (doc is null)
                    {
                        return ErrorPrepare("file_not_in_solution", "Could not find file in loaded solution documents.");
                    }

                    (RenameCandidate? candidate, string? errorCode, string? message) =
                        await ResolveRenameCandidateAsync(doc, line, column, cts.Token);

                    if (candidate is null)
                    {
                        return ErrorPrepare(
                            errorCode ?? "invalid_rename_target",
                            message ?? "Cannot determine a valid rename target.");
                    }

                    if (!CanRenameSymbol(candidate.Symbol))
                    {
                        return ErrorPrepare(
                            "unsupported_symbol_kind",
                            $"Symbol kind '{candidate.Symbol.Kind}' is not supported for rename.");
                    }

                    if (!IsSourceSymbol(candidate.Symbol))
                    {
                        return ErrorPrepare("symbol_not_in_source", "Can only rename symbols declared in source files.");
                    }

                    return new RenamePrepareResult
                    {
                        Success = true,
                        Placeholder = candidate.Placeholder,
                        SymbolKind = candidate.Symbol.Kind.ToString(),
                        StartLine = candidate.StartLine,
                        StartColumn = candidate.StartColumn,
                        EndLine = candidate.EndLine,
                        EndColumn = candidate.EndColumn,
                        Message = "Rename can be prepared."
                    };
                }
            }
            catch (OperationCanceledException)
            {
                return ErrorPrepare("operation_timeout", "Prepare rename operation timed out.");
            }
            catch (ArgumentException ex)
            {
                return ErrorPrepare("invalid_argument", ex.Message);
            }
            catch (UnauthorizedAccessException ex)
            {
                return ErrorPrepare("access_denied", ex.Message);
            }
            catch (IOException ex)
            {
                return ErrorPrepare("io_error", ex.Message);
            }
            catch (InvalidOperationException ex)
            {
                return ErrorPrepare("invalid_operation", ex.Message);
            }
            catch (Exception ex)
            {
                return ErrorPrepare("unexpected_error", ex.Message);
            }
        }

        private static bool CanRenameSymbol(ISymbol symbol)
        {
            if (symbol is not { CanBeReferencedByName: true })
            {
                return false;
            }

            if (!SupportedSymbolKinds.Contains(symbol.Kind))
            {
                return false;
            }

            if (symbol is IPropertySymbol propertySymbol && propertySymbol.IsIndexer)
            {
                return false;
            }

            if (symbol is IMethodSymbol methodSymbol)
            {
                if (methodSymbol.MethodKind is MethodKind.Constructor or MethodKind.StaticConstructor or MethodKind.Destructor)
                {
                    return false;
                }
            }

            return true;
        }

        private static bool IsSourceSymbol(ISymbol symbol) => symbol.Locations.Any(location => location.IsInSource);

        private static bool IsValidCSharpIdentifier(string newName)
        {
            if (string.IsNullOrWhiteSpace(newName))
            {
                return false;
            }

            return SyntaxFacts.IsValidIdentifier(newName);
        }

        private static bool IsSupportedSolutionFile(string solutionPath)
        {
            string extension = Path.GetExtension(solutionPath);
            return string.Equals(extension, ".sln", StringComparison.OrdinalIgnoreCase)
                || string.Equals(extension, ".slnx", StringComparison.OrdinalIgnoreCase);
        }

        private static Document? FindDocument(Solution solution, string normalizedFilePath)
        {
            return solution.Projects
                .SelectMany(project => project.Documents)
                .FirstOrDefault(document =>
                    !string.IsNullOrWhiteSpace(document.FilePath)
                    && string.Equals(Path.GetFullPath(document.FilePath), normalizedFilePath, StringComparison.OrdinalIgnoreCase));
        }

        private static async Task<(RenameCandidate? candidate, string? errorCode, string? message)> ResolveRenameCandidateAsync(
            Document document,
            int line,
            int column,
            CancellationToken token)
        {
            SourceText sourceText = await document.GetTextAsync(token);

            int zeroLine = line - 1;
            int zeroColumn = column - 1;

            if (zeroLine >= sourceText.Lines.Count)
            {
                return (null, "invalid_position", "line is beyond file bounds.");
            }

            TextLine textLine = sourceText.Lines[zeroLine];
            if (zeroColumn > textLine.ToString().Length)
            {
                return (null, "invalid_position", "column is beyond selected line length.");
            }

            int position = sourceText.Lines.GetPosition(new LinePosition(zeroLine, zeroColumn));
            SyntaxNode? root = await document.GetSyntaxRootAsync(token);

            if (root is null)
            {
                return (null, "invalid_document", "Could not read syntax tree for document.");
            }

            SyntaxNode? nodeOnPos = root.FindNode(new TextSpan(position, 0), findInsideTrivia: false, getInnermostNodeForTie: true);
            if (nodeOnPos is null)
            {
                return (null, "invalid_rename_target", "No syntax node found at the provided position.");
            }

            if (!TryGetRenameSpan(nodeOnPos, out TextSpan renameSpan, out string placeholder))
            {
                return (null, "invalid_rename_target", "This syntax node cannot be renamed.");
            }

            ISymbol? symbol = await SymbolFinder.FindSymbolAtPositionAsync(document, position, token);
            if (symbol is null)
            {
                return (null, "no_symbol_at_position", "No symbol found at provided position.");
            }

            LinePosition startLinePosition = sourceText.Lines.GetLinePosition(renameSpan.Start);
            LinePosition endLinePosition = sourceText.Lines.GetLinePosition(renameSpan.End);

            return (
                new RenameCandidate
                {
                    Document = document,
                    Symbol = symbol,
                    RenameSpan = renameSpan,
                    Placeholder = placeholder,
                    StartLine = startLinePosition.Line + 1,
                    StartColumn = startLinePosition.Character + 1,
                    EndLine = endLinePosition.Line + 1,
                    EndColumn = endLinePosition.Character + 1
                },
                null,
                null);
        }

        private static async Task<(RenameCandidate? candidate, string? errorCode, string? message)> ResolveRenameCandidateAsync(
            Document document,
            int lineNumber,
            string oldName,
            CancellationToken token)
        {
            if (string.IsNullOrWhiteSpace(oldName))
            {
                return (null, "invalid_old_name", "oldName must be provided.");
            }

            SourceText sourceText = await document.GetTextAsync(token);

            int zeroLine = lineNumber - 1;
            if (zeroLine < 0 || zeroLine >= sourceText.Lines.Count)
            {
                return (null, "invalid_line_number", "lineNumber is beyond file bounds.");
            }

            TextLine textLine = sourceText.Lines[zeroLine];
            SyntaxNode? root = await document.GetSyntaxRootAsync(token);
            if (root is null)
            {
                return (null, "invalid_document", "Could not read syntax tree for document.");
            }

            string normalizedOldName = NormalizeIdentifierText(oldName);
            List<RenameCandidate> candidates = new();

            foreach (SyntaxToken tokenOnLine in root.DescendantTokens(textLine.Span, descendIntoTrivia: false))
            {
                if (!tokenOnLine.IsKind(SyntaxKind.IdentifierToken))
                {
                    continue;
                }

                if (!string.Equals(tokenOnLine.ValueText, normalizedOldName, StringComparison.Ordinal)
                    && !string.Equals(tokenOnLine.Text, oldName, StringComparison.Ordinal))
                {
                    continue;
                }

                SyntaxNode? nodeOnPos = tokenOnLine.Parent;
                if (nodeOnPos is null)
                {
                    continue;
                }

                if (!TryGetRenameSpan(nodeOnPos, out TextSpan renameSpan, out string placeholder))
                {
                    continue;
                }

                ISymbol? symbol = await SymbolFinder.FindSymbolAtPositionAsync(document, tokenOnLine.SpanStart, token);
                if (symbol is null)
                {
                    continue;
                }

                LinePosition startLinePosition = sourceText.Lines.GetLinePosition(renameSpan.Start);
                LinePosition endLinePosition = sourceText.Lines.GetLinePosition(renameSpan.End);

                candidates.Add(
                    new RenameCandidate
                    {
                        Document = document,
                        Symbol = symbol,
                        RenameSpan = renameSpan,
                        Placeholder = placeholder,
                        StartLine = startLinePosition.Line + 1,
                        StartColumn = startLinePosition.Character + 1,
                        EndLine = endLinePosition.Line + 1,
                        EndColumn = endLinePosition.Character + 1
                    });
            }

            if (candidates.Count == 0)
            {
                return (null, "old_name_not_found_on_line", $"No renameable symbol named '{oldName}' was found on line {lineNumber}.");
            }

            List<RenameCandidate> distinctCandidates = new();
            HashSet<ISymbol> seenSymbols = new(SymbolEqualityComparer.Default);
            foreach (RenameCandidate candidate in candidates.OrderBy(candidate => candidate.StartColumn).ThenBy(candidate => candidate.StartLine))
            {
                if (seenSymbols.Add(candidate.Symbol))
                {
                    distinctCandidates.Add(candidate);
                }
            }

            if (distinctCandidates.Count > 1)
            {
                return (null, "ambiguous_old_name_on_line", $"Multiple renameable symbols named '{oldName}' were found on line {lineNumber}.");
            }

            RenameCandidate selectedCandidate = distinctCandidates[0];
            return (selectedCandidate, null, null);
        }

        private static async Task ApplyRenamedSolutionToDiskAsync(
            Solution originalSolution,
            Solution renamedSolution,
            string? fileMoveFromPath,
            string? fileMoveToPath,
            CancellationToken token)
        {
            // MSBuildWorkspace.TryApplyChanges throws for rename results that include document-property moves.
            // We persist the computed snapshot directly to disk so git sees an actual rename/move instead of a
            // delete+add pair. This path assumes the project discovers source files from disk (SDK-style globbing);
            // explicit compile-item updates remain a later enhancement if we need non-globbed projects.
            foreach (Project originalProject in originalSolution.Projects)
            {
                foreach (Document originalDocument in originalProject.Documents)
                {
                    if (string.IsNullOrWhiteSpace(originalDocument.FilePath))
                    {
                        continue;
                    }

                    Document? renamedDocument = renamedSolution.GetDocument(originalDocument.Id);
                    if (renamedDocument is null || string.IsNullOrWhiteSpace(renamedDocument.FilePath))
                    {
                        continue;
                    }

                    string originalFilePath = Path.GetFullPath(originalDocument.FilePath);
                    string renamedFilePath = Path.GetFullPath(renamedDocument.FilePath);
                    bool plannedFileMove = !string.IsNullOrWhiteSpace(fileMoveFromPath)
                        && !string.IsNullOrWhiteSpace(fileMoveToPath)
                        && string.Equals(originalFilePath, Path.GetFullPath(fileMoveFromPath), StringComparison.OrdinalIgnoreCase);
                    if (plannedFileMove)
                    {
                        renamedFilePath = Path.GetFullPath(fileMoveToPath!);
                    }

                    SourceText originalText = await originalDocument.GetTextAsync(token);
                    SourceText renamedText = await renamedDocument.GetTextAsync(token);
                    bool textChanged = originalText.GetTextChanges(renamedText).Any();
                    bool fileMoved = plannedFileMove || !string.Equals(originalFilePath, renamedFilePath, StringComparison.OrdinalIgnoreCase);

                    if (!textChanged && !fileMoved)
                    {
                        continue;
                    }

                    if (fileMoved)
                    {
                        string? destinationDirectory = Path.GetDirectoryName(renamedFilePath);
                        if (!string.IsNullOrWhiteSpace(destinationDirectory))
                        {
                            Directory.CreateDirectory(destinationDirectory);
                        }

                        if (File.Exists(renamedFilePath))
                        {
                            throw new IOException($"Destination file already exists: {renamedFilePath}");
                        }

                        File.Move(originalFilePath, renamedFilePath);
                    }

                    await File.WriteAllTextAsync(renamedFilePath, renamedText.ToString(), token);
                }
            }
        }

        private static (string? FromPath, string? ToPath) GetFileRenamePlan(
            Document document,
            ISymbol symbol,
            string newName,
            bool renameFile)
        {
            if (!renameFile)
            {
                return (null, null);
            }

            if (symbol is not INamedTypeSymbol namedTypeSymbol)
            {
                return (null, null);
            }

            if (namedTypeSymbol.DeclaringSyntaxReferences.Length != 1)
            {
                return (null, null);
            }

            if (string.IsNullOrWhiteSpace(document.FilePath))
            {
                return (null, null);
            }

            string originalFilePath = Path.GetFullPath(document.FilePath);
            string currentFileStem = NormalizeIdentifierText(Path.GetFileNameWithoutExtension(originalFilePath));
            string symbolStem = NormalizeIdentifierText(symbol.Name);
            if (!string.Equals(currentFileStem, symbolStem, StringComparison.Ordinal))
            {
                return (null, null);
            }

            string targetFileStem = NormalizeIdentifierText(newName);
            string targetFilePath = Path.Combine(Path.GetDirectoryName(originalFilePath) ?? string.Empty, $"{targetFileStem}{Path.GetExtension(originalFilePath)}");
            targetFilePath = Path.GetFullPath(targetFilePath);
            if (string.Equals(originalFilePath, targetFilePath, StringComparison.OrdinalIgnoreCase))
            {
                return (null, null);
            }

            return (originalFilePath, targetFilePath);
        }

        private static bool TryGetRenameSpan(SyntaxNode node, out TextSpan span, out string text)
        {
            if (node is IdentifierNameSyntax identifierName)
            {
                span = identifierName.Identifier.Span;
                text = identifierName.Identifier.Text;
                return true;
            }

            if (node is GenericNameSyntax genericName)
            {
                span = genericName.Identifier.Span;
                text = genericName.Identifier.Text;
                return true;
            }

            if (node is QualifiedNameSyntax qualifiedName)
            {
                span = qualifiedName.Right.Span;
                text = qualifiedName.Right.ToString();
                return true;
            }

            if (node is AliasQualifiedNameSyntax aliasQualifiedName)
            {
                span = aliasQualifiedName.Name.Span;
                text = aliasQualifiedName.Name.ToString();
                return true;
            }

            switch (node)
            {
                case NamespaceDeclarationSyntax namespaceDeclaration:
                    span = namespaceDeclaration.Name.Span;
                    text = namespaceDeclaration.Name.ToString();
                    return true;

                case FileScopedNamespaceDeclarationSyntax fileScopedNamespaceDeclaration:
                    span = fileScopedNamespaceDeclaration.Name.Span;
                    text = fileScopedNamespaceDeclaration.Name.ToString();
                    return true;

                case PropertyDeclarationSyntax propertyDeclaration:
                    span = propertyDeclaration.Identifier.Span;
                    text = propertyDeclaration.Identifier.Text;
                    return true;

                case MethodDeclarationSyntax methodDeclaration:
                    span = methodDeclaration.Identifier.Span;
                    text = methodDeclaration.Identifier.Text;
                    return true;

                case BaseTypeDeclarationSyntax typeDeclaration:
                    span = typeDeclaration.Identifier.Span;
                    text = typeDeclaration.Identifier.Text;
                    return true;

                case VariableDeclaratorSyntax variableDeclaration:
                    span = variableDeclaration.Identifier.Span;
                    text = variableDeclaration.Identifier.Text;
                    return true;

                case EnumMemberDeclarationSyntax enumMemberDeclaration:
                    span = enumMemberDeclaration.Identifier.Span;
                    text = enumMemberDeclaration.Identifier.Text;
                    return true;

                case ParameterSyntax parameterSyntax:
                    span = parameterSyntax.Identifier.Span;
                    text = parameterSyntax.Identifier.Text;
                    return true;

                case TypeParameterSyntax typeParameterSyntax:
                    span = typeParameterSyntax.Identifier.Span;
                    text = typeParameterSyntax.Identifier.Text;
                    return true;

                case SingleVariableDesignationSyntax singleVariableDesignation:
                    span = singleVariableDesignation.Identifier.Span;
                    text = singleVariableDesignation.Identifier.Text;
                    return true;

                case ForEachStatementSyntax forEachStatement:
                    span = forEachStatement.Identifier.Span;
                    text = forEachStatement.Identifier.Text;
                    return true;

                case LocalFunctionStatementSyntax localFunction:
                    span = localFunction.Identifier.Span;
                    text = localFunction.Identifier.Text;
                    return true;

                case ConstructorDeclarationSyntax constructorDeclaration:
                    span = constructorDeclaration.Identifier.Span;
                    text = constructorDeclaration.Identifier.Text;
                    return true;

                default:
                    break;
            }

            span = default;
            text = string.Empty;
            return false;
        }

        private static string NormalizeIdentifierText(string name)
        {
            return name.StartsWith("@", StringComparison.Ordinal) ? name[1..] : name;
        }

        private static CancellationTokenSource CreateCancellationTokenSource(int timeoutSeconds)
        {
            if (timeoutSeconds < MinTimeoutSeconds || timeoutSeconds > MaxTimeoutSeconds)
            {
                timeoutSeconds = DefaultTimeoutSeconds;
            }

            return new CancellationTokenSource(TimeSpan.FromSeconds(timeoutSeconds));
        }

        private static RenameResult Error(string code, string message) => new()
        {
            Success = false,
            ErrorCode = code,
            Message = message
        };

        private static RenamePrepareResult ErrorPrepare(string code, string message) => new()
        {
            Success = false,
            ErrorCode = code,
            Message = message
        };
    }
}
