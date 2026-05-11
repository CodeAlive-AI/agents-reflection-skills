using CSharpRefactoring.Core;
using System;

namespace CSharpRefactoring.Cli;

internal static class Program
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
            bool dryRun = args.Length < 7 || (bool.TryParse(args[6], out bool parsedDryRun) && parsedDryRun);

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
        Console.WriteLine("  rename-symbol <sln> <file> <line> <oldName> <newName> [dryRun=true|false]");
    }
}
