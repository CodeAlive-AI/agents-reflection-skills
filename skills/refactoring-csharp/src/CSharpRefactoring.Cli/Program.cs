using CSharpRefactoring.Core;
using System;

namespace CSharpRefactoring.Cli;

public static class Program
{
    public static int Main(string[] args)
    {
        return MainAsync(args).GetAwaiter().GetResult();
    }

    private static async Task<int> MainAsync(string[] args)
    {
        if (args.Length < 2)
        {
            PrintUsage();
            return 0;
        }

        string command = args[0];
        if (string.Equals(command, "rename-symbol", StringComparison.OrdinalIgnoreCase))
        {
            if (args.Length < 6)
            {
                PrintUsage();
                return 1;
            }

            string solutionPath = Path.GetFullPath(args[1]);
            string filePath = Path.GetFullPath(args[2]);

            if (!int.TryParse(args[3], out int lineNumber))
            {
                Console.WriteLine("line must be a number.");
                return 1;
            }

            string oldName = args[4];
            string newName = args[5];
            if (args.Length > 7)
            {
                Console.WriteLine("Too many arguments.");
                PrintUsage();
                return 1;
            }

            if (!TryParseDryRunArgument(args.Length >= 7 ? args[6] : null, out bool dryRun, out string? dryRunError))
            {
                Console.WriteLine(dryRunError);
                PrintUsage();
                return 1;
            }

            var result = await CSharpSymbolRenamer.Tool.RenameSymbol(
                solutionPath,
                filePath,
                lineNumber,
                oldName,
                newName,
                dryRun: dryRun);

            if (!result.Success)
            {
                Console.WriteLine($"FAIL [{result.ErrorCode}]: {result.Message}");
                return 2;
            }

            Console.WriteLine($"Mode: {result.Mode}");
            Console.WriteLine(result.Message);
            Console.WriteLine($"Range: ({result.StartLine},{result.StartColumn})-({result.EndLine},{result.EndColumn})");
            Console.WriteLine($"Symbol: {result.SymbolDisplay} ({result.SymbolKind})");
            Console.WriteLine($"Documents: {result.ChangedDocumentCount}, Text changes: {result.TotalTextChanges}");
            if (!string.IsNullOrWhiteSpace(result.FileMoveFromPath) && !string.IsNullOrWhiteSpace(result.FileMoveToPath))
            {
                Console.WriteLine($"File move: {result.FileMoveFromPath} -> {result.FileMoveToPath}");
            }
            foreach (var doc in result.ChangedDocuments)
            {
                Console.WriteLine($" - {doc.FilePath} ({doc.Changes} text changes)");
            }

            return 0;
        }

        Console.WriteLine("Only 'rename-symbol' is supported.");
        return 1;
    }

    private static void PrintUsage()
    {
        Console.WriteLine("Usage:");
        Console.WriteLine("  rename-symbol <sln> <file> <line> <oldName> <newName> [dryRun=false|true]");
    }

    public static bool TryParseDryRunArgument(string? argument, out bool dryRun, out string? error)
    {
        dryRun = false;
        error = null;

        if (string.IsNullOrWhiteSpace(argument))
        {
            return true;
        }

        string value = argument.Trim();

        if (string.Equals(value, "--dry-run", StringComparison.OrdinalIgnoreCase))
        {
            dryRun = true;
            return true;
        }

        if (string.Equals(value, "--no-dry-run", StringComparison.OrdinalIgnoreCase))
        {
            dryRun = false;
            return true;
        }

        const string dryRunPrefix = "dryRun=";
        const string dryRunKebabPrefix = "--dry-run=";
        if (value.StartsWith(dryRunPrefix, StringComparison.OrdinalIgnoreCase))
        {
            value = value[dryRunPrefix.Length..];
        }
        else if (value.StartsWith(dryRunKebabPrefix, StringComparison.OrdinalIgnoreCase))
        {
            value = value[dryRunKebabPrefix.Length..];
        }

        if (bool.TryParse(value, out dryRun))
        {
            return true;
        }

        error = $"Invalid dryRun argument '{argument}'. Use true, false, dryRun=true, dryRun=false, --dry-run, or --no-dry-run.";
        return false;
    }
}
