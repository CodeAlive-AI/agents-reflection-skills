using CSharpRefactoring.Core;
using System;
using System.IO;
using Xunit;

namespace CSharpRefactoring.Core.Tests;

public sealed class CSharpSymbolRenamerTests
{
    private const string TestDataRootFolderName = "TestData";
    private const string SampleSolutionFolder = "SampleRenameDemo";
    private const string SampleSolutionFile = "SampleRenameDemo.sln";
    private const string SampleProgramFile = "Program.cs";

    [Fact]
    public async Task RenameSymbol_DryRun_ReportsExpectedChanges_ForProperty()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);

        int lineNumber = FindLineNumber(filePath, "public string DisplayName");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            filePath,
            lineNumber,
            "DisplayName",
            "DisplayTitle",
            dryRun: true);

        Assert.True(result.Success);
        Assert.True(result.DryRun);
        Assert.Equal("dry_run", result.Mode);
        Assert.Equal("DisplayName", result.OriginalName);
        Assert.Equal("DisplayTitle", result.NewName);
        Assert.True(result.ChangedDocumentCount >= 1);
        Assert.True(result.TotalTextChanges > 0);
        Assert.Null(result.ErrorCode);
    }

    [Fact]
    public async Task RenameSymbol_Defaults_RenameFileAndComments_ButNotStrings()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        string solutionPath = Path.Combine(workingDirectory, SampleSolutionFile);
        string trackedFilePath = Path.Combine(workingDirectory, "ProjectWidget.cs");
        File.WriteAllText(
            trackedFilePath,
            """
            public class ProjectWidget
            {
                // ProjectWidget should be renamed in comments.
                public string Label => "ProjectWidget";
            }
            """);

        int lineNumber = FindLineNumber(trackedFilePath, "public class ProjectWidget");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            trackedFilePath,
            lineNumber,
            "ProjectWidget",
            "RenamedWidget",
            dryRun: false);

        Assert.True(result.Success);
        Assert.Equal("applied", result.Mode);
        Assert.Equal("ProjectWidget", result.OriginalName);
        Assert.Equal("RenamedWidget", result.NewName);
        Assert.Equal(Path.GetFullPath(trackedFilePath), result.FileMoveFromPath);
        Assert.Equal(Path.GetFullPath(Path.Combine(workingDirectory, "RenamedWidget.cs")), result.FileMoveToPath);
        Assert.False(File.Exists(trackedFilePath));
        Assert.True(File.Exists(result.FileMoveToPath!));

        string updatedCode = await File.ReadAllTextAsync(result.FileMoveToPath!);
        Assert.Contains("// RenamedWidget should be renamed in comments.", updatedCode);
        Assert.Contains("=> \"ProjectWidget\";", updatedCode);
        Assert.DoesNotContain("public class ProjectWidget", updatedCode);
    }

    [Fact]
    public async Task RenameSymbol_Updates_AllUsages_ForMethod()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);

        int lineNumber = FindLineNumber(filePath, "public int CountMethod()");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            filePath,
            lineNumber,
            "CountMethod",
            "GetTotalCount",
            dryRun: false);

        Assert.True(result.Success);
        Assert.Equal("applied", result.Mode);
        Assert.False(result.DryRun);
        Assert.Equal(1, result.ChangedDocumentCount);
        Assert.True(result.TotalTextChanges > 0);

        string updatedCode = await File.ReadAllTextAsync(filePath);
        Assert.Contains("GetTotalCount", updatedCode);
        Assert.DoesNotContain("CountMethod()", updatedCode);
        Assert.Contains("GetTotalCount()", updatedCode);
        Assert.DoesNotContain("CountMethod =", updatedCode, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public async Task RenameSymbol_ReturnsError_WhenNewNameIsSameAsCurrent()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);

        int lineNumber = FindLineNumber(filePath, "public string DisplayName");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            filePath,
            lineNumber,
            "DisplayName",
            "DisplayName");

        Assert.False(result.Success);
        Assert.Equal("same_name", result.ErrorCode);
    }

    [Fact]
    public async Task RenameSymbol_ReturnsError_WhenOldNameDoesNotMatchLine()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);

        int lineNumber = FindLineNumber(filePath, "public string DisplayName");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            filePath,
            lineNumber,
            "MissingSymbol",
            "Anything");

        Assert.False(result.Success);
        Assert.Equal("old_name_not_found_on_line", result.ErrorCode);
    }

    [Fact]
    public async Task RenameSymbol_ReturnsError_WhenLineNumberIsInvalid()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            filePath,
            lineNumber: 0,
            "DisplayName",
            "Anything");

        Assert.False(result.Success);
        Assert.Equal("invalid_line_number", result.ErrorCode);
    }

    [Fact]
    public async Task RenameSymbol_ReturnsError_WhenSymbolIsUnsupported()
    {
        string workingDirectory = CreateWorkingCopyFromTestData();
        (string solutionPath, string filePath) = GetPaths(workingDirectory);
        AddUnsupportedConstructorFixture(workingDirectory);

        string unsupportedFilePath = Path.Combine(workingDirectory, "UnsupportedCase.cs");
        int lineNumber = FindLineNumber(unsupportedFilePath, "public UnsupportedCase()");

        CSharpSymbolRenamer.RenameResult result = await CSharpSymbolRenamer.Tool.RenameSymbol(
            solutionPath,
            unsupportedFilePath,
            lineNumber,
            "UnsupportedCase",
            "NewUnsupportedCase");

        Assert.False(result.Success);
        Assert.Equal("unsupported_symbol_kind", result.ErrorCode);
    }

    private static string CreateWorkingCopyFromTestData()
    {
        string sourceDirectory = LocateTestDataDirectory();

        string workingDirectory = Path.Combine(
            Path.GetTempPath(),
            "CSharpRefactoring.Core.Tests",
            Guid.NewGuid().ToString("N"));

        CopyDirectory(sourceDirectory, workingDirectory);
        return workingDirectory;
    }

    private static (string SolutionPath, string ProgramFilePath) GetPaths(string workingDirectory)
    {
        string solutionPath = Path.Combine(workingDirectory, SampleSolutionFile);
        string filePath = Path.Combine(workingDirectory, SampleProgramFile);
        return (solutionPath, filePath);
    }

    private static int FindLineNumber(string filePath, string marker)
    {
        string text = File.ReadAllText(filePath);
        int markerIndex = text.IndexOf(marker, StringComparison.Ordinal);
        Assert.True(markerIndex >= 0, $"Marker '{marker}' not found in {filePath}");

        string beforeMarker = text[..markerIndex];
        return beforeMarker.Count(c => c == '\n') + 1;
    }

    private static void AddUnsupportedConstructorFixture(string workingDirectory)
    {
        const string constructorFileContent = """
            public class UnsupportedCase
            {
                public UnsupportedCase()
                {
                }
            }

            """;

        string ctorFilePath = Path.Combine(workingDirectory, "UnsupportedCase.cs");
        File.WriteAllText(ctorFilePath, constructorFileContent);
        Assert.True(File.Exists(ctorFilePath));
    }

    private static void CopyDirectory(string sourcePath, string destinationPath)
    {
        Directory.CreateDirectory(destinationPath);
        foreach (string file in Directory.GetFiles(sourcePath, "*", SearchOption.AllDirectories))
        {
            string relative = Path.GetRelativePath(sourcePath, file);
            string destinationFile = Path.Combine(destinationPath, relative);
            string destinationDirectory = Path.GetDirectoryName(destinationFile)!;
            Directory.CreateDirectory(destinationDirectory);
            File.Copy(file, destinationFile);
        }
    }

    private static string LocateTestDataDirectory()
    {
        DirectoryInfo? directory = new DirectoryInfo(AppContext.BaseDirectory);
        while (directory is not null)
        {
            string candidate = Path.Combine(directory.FullName, TestDataRootFolderName, SampleSolutionFolder);
            if (Directory.Exists(candidate))
            {
                return candidate;
            }

            directory = directory.Parent;
        }

        throw new DirectoryNotFoundException($"Could not locate {TestDataRootFolderName}/{SampleSolutionFolder} from base path {AppContext.BaseDirectory}");
    }
}
