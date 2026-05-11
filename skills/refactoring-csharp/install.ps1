param(
    [switch]$Codex,
    [switch]$Claude,
    [switch]$All,
    [switch]$NoBinary,
    [string]$Source
)

$ErrorActionPreference = "Stop"

$Repo = "CodeAlive-AI/ai-driven-development"
$SkillName = "refactoring-csharp"
$SkillAsset = "refactoring-csharp-skill.tar.gz"

if (-not $Codex -and -not $Claude -and -not $All) {
    $All = $true
}

function Resolve-Tag {
    if ($env:REFACTORING_CSHARP_VERSION) {
        return $env:REFACTORING_CSHARP_VERSION
    }

    $releases = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases?per_page=50"
    $release = $releases | Where-Object { $_.tag_name -like "refactoring-csharp-v*" } | Select-Object -First 1
    if (-not $release) {
        throw "No refactoring-csharp-v* release found in $Repo"
    }

    return $release.tag_name
}

function Copy-SkillFromSource {
    param([string]$From, [string]$To)

    if (Test-Path $To) {
        Remove-Item -Recurse -Force $To
    }
    New-Item -ItemType Directory -Force -Path $To | Out-Null

    Get-ChildItem -LiteralPath $From -Force |
        Where-Object { $_.Name -notin @("bin", "obj", "dist") } |
        ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $To -Recurse -Force
        }

    Get-ChildItem -LiteralPath $To -Directory -Recurse -Force |
        Where-Object { $_.Name -in @("bin", "obj") } |
        Remove-Item -Recurse -Force
}

function Install-SkillArchive {
    param([string]$Tag, [string]$To)

    $tmp = New-Item -ItemType Directory -Force -Path ([System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString("N")))
    try {
        $archive = Join-Path $tmp.FullName $SkillAsset
        Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repo/releases/download/$Tag/$SkillAsset" -OutFile $archive
        if (Test-Path $To) {
            Remove-Item -Recurse -Force $To
        }
        New-Item -ItemType Directory -Force -Path $To | Out-Null
        tar -xzf $archive -C $To
    }
    finally {
        Remove-Item -Recurse -Force $tmp.FullName -ErrorAction SilentlyContinue
    }
}

function Install-Binary {
    param([string]$Tag, [string]$To)

    $tmp = New-Item -ItemType Directory -Force -Path ([System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString("N")))
    try {
        $asset = "csharp-refactor-win-x64.zip"
        $archive = Join-Path $tmp.FullName $asset
        $sums = Join-Path $tmp.FullName "SHA256SUMS"
        Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repo/releases/download/$Tag/$asset" -OutFile $archive
        Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repo/releases/download/$Tag/SHA256SUMS" -OutFile $sums

        $expected = (Get-Content $sums | Where-Object { $_ -match "\s$asset$" } | Select-Object -First 1).Split(" ")[0]
        $actual = (Get-FileHash -Algorithm SHA256 $archive).Hash.ToLowerInvariant()
        if ($actual -ne $expected.ToLowerInvariant()) {
            throw "Checksum mismatch for $asset"
        }

        $binDir = Join-Path $To "bin"
        New-Item -ItemType Directory -Force -Path $binDir | Out-Null
        Expand-Archive -LiteralPath $archive -DestinationPath $tmp.FullName -Force
        Move-Item -Force -LiteralPath (Join-Path $tmp.FullName "csharp-refactor.exe") -Destination (Join-Path $binDir "csharp-refactor.exe")
    }
    finally {
        Remove-Item -Recurse -Force $tmp.FullName -ErrorAction SilentlyContinue
    }
}

$destinations = @()
if ($All -or $Codex) {
    $destinations += Join-Path $HOME ".codex\skills\$SkillName"
}
if ($All -or $Claude) {
    $destinations += Join-Path $HOME ".claude\skills\$SkillName"
}

$tag = $null
if (-not $Source) {
    $tag = Resolve-Tag
}
elseif (-not (Test-Path $Source)) {
    throw "Source path does not exist: $Source"
}

foreach ($dest in $destinations) {
    Write-Host "Installing $SkillName -> $dest"
    if ($Source) {
        Copy-SkillFromSource -From $Source -To $dest
    }
    else {
        Install-SkillArchive -Tag $tag -To $dest
    }

    if (-not $NoBinary -and $tag) {
        Install-Binary -Tag $tag -To $dest
        Write-Host "  binary: $(Join-Path $dest 'bin\csharp-refactor.exe')"
    }
}

Write-Host ""
Write-Host "Done. Restart the agent if this is a new skill installation."
