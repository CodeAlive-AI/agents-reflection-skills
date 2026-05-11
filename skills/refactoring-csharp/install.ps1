param(
    [string[]]$Agent = @(),
    [switch]$Codex,
    [switch]$Claude,
    [switch]$All,
    [switch]$AllAgents,
    [switch]$Detected,
    [switch]$NoBinary,
    [string]$Source
)

$ErrorActionPreference = "Stop"

$Repo = "CodeAlive-AI/ai-driven-development"
$SkillName = "refactoring-csharp"
$SkillAsset = "refactoring-csharp-skill.tar.gz"

$AgentIds = @(
    "adal", "amp", "antigravity", "augment", "claude-code", "cline", "codebuddy", "codex", "command-code",
    "continue", "crush", "cursor", "droid", "gemini-cli", "github-copilot", "goose", "iflow-cli", "junie",
    "kilo", "kimi-cli", "kiro-cli", "kode", "mcpjam", "mistral-vibe", "mux", "neovate", "openclaw", "opencode",
    "openhands", "pi", "pochi", "qoder", "qwen-code", "replit", "roo", "trae", "trae-cn", "windsurf", "zencoder"
)

function Normalize-AgentId {
    param([string]$Id)
    switch ($Id) {
        "claude" { "claude-code"; break }
        "gemini" { "gemini-cli"; break }
        "copilot" { "github-copilot"; break }
        "iflow" { "iflow-cli"; break }
        "kimi" { "kimi-cli"; break }
        "kiro" { "kiro-cli"; break }
        "qwen" { "qwen-code"; break }
        default { $Id }
    }
}

function Get-AgentSkillDir {
    param([string]$Id)
    switch ($Id) {
        "adal" { Join-Path $HOME ".adal\skills\$SkillName"; break }
        "amp" { Join-Path $HOME ".config\agents\skills\$SkillName"; break }
        "antigravity" { Join-Path $HOME ".gemini\antigravity\skills\$SkillName"; break }
        "augment" { Join-Path $HOME ".augment\skills\$SkillName"; break }
        "claude-code" { Join-Path $HOME ".claude\skills\$SkillName"; break }
        "cline" { Join-Path $HOME ".cline\skills\$SkillName"; break }
        "codebuddy" { Join-Path $HOME ".codebuddy\skills\$SkillName"; break }
        "codex" { Join-Path $HOME ".codex\skills\$SkillName"; break }
        "command-code" { Join-Path $HOME ".commandcode\skills\$SkillName"; break }
        "continue" { Join-Path $HOME ".continue\skills\$SkillName"; break }
        "crush" { Join-Path $HOME ".config\crush\skills\$SkillName"; break }
        "cursor" { Join-Path $HOME ".cursor\skills\$SkillName"; break }
        "droid" { Join-Path $HOME ".factory\skills\$SkillName"; break }
        "gemini-cli" { Join-Path $HOME ".gemini\skills\$SkillName"; break }
        "github-copilot" { Join-Path $HOME ".copilot\skills\$SkillName"; break }
        "goose" { Join-Path $HOME ".config\goose\skills\$SkillName"; break }
        "iflow-cli" { Join-Path $HOME ".iflow\skills\$SkillName"; break }
        "junie" { Join-Path $HOME ".junie\skills\$SkillName"; break }
        "kilo" { Join-Path $HOME ".kilocode\skills\$SkillName"; break }
        "kimi-cli" { Join-Path $HOME ".config\agents\skills\$SkillName"; break }
        "kiro-cli" { Join-Path $HOME ".kiro\skills\$SkillName"; break }
        "kode" { Join-Path $HOME ".kode\skills\$SkillName"; break }
        "mcpjam" { Join-Path $HOME ".mcpjam\skills\$SkillName"; break }
        "mistral-vibe" { Join-Path $HOME ".vibe\skills\$SkillName"; break }
        "mux" { Join-Path $HOME ".mux\skills\$SkillName"; break }
        "neovate" { Join-Path $HOME ".neovate\skills\$SkillName"; break }
        "openclaw" { Join-Path $HOME ".openclaw\skills\$SkillName"; break }
        "opencode" { Join-Path $HOME ".config\opencode\skills\$SkillName"; break }
        "openhands" { Join-Path $HOME ".openhands\skills\$SkillName"; break }
        "pi" { Join-Path $HOME ".pi\agent\skills\$SkillName"; break }
        "pochi" { Join-Path $HOME ".pochi\skills\$SkillName"; break }
        "qoder" { Join-Path $HOME ".qoder\skills\$SkillName"; break }
        "qwen-code" { Join-Path $HOME ".qwen\skills\$SkillName"; break }
        "replit" { Join-Path $HOME ".config\agents\skills\$SkillName"; break }
        "roo" { Join-Path $HOME ".roo\skills\$SkillName"; break }
        "trae" { Join-Path $HOME ".trae\skills\$SkillName"; break }
        "trae-cn" { Join-Path $HOME ".trae-cn\skills\$SkillName"; break }
        "windsurf" { Join-Path $HOME ".codeium\windsurf\skills\$SkillName"; break }
        "zencoder" { Join-Path $HOME ".zencoder\skills\$SkillName"; break }
        default { throw "Unsupported agent id: $Id" }
    }
}

function Get-AgentConfigDir {
    param([string]$Id)
    switch ($Id) {
        "adal" { Join-Path $HOME ".adal"; break }
        { $_ -in @("amp", "kimi-cli", "replit") } { Join-Path $HOME ".config\agents"; break }
        "antigravity" { Join-Path $HOME ".gemini\antigravity"; break }
        "augment" { Join-Path $HOME ".augment"; break }
        "claude-code" { Join-Path $HOME ".claude"; break }
        "cline" { Join-Path $HOME ".cline"; break }
        "codebuddy" { Join-Path $HOME ".codebuddy"; break }
        "codex" { Join-Path $HOME ".codex"; break }
        "command-code" { Join-Path $HOME ".commandcode"; break }
        "continue" { Join-Path $HOME ".continue"; break }
        "crush" { Join-Path $HOME ".config\crush"; break }
        "cursor" { Join-Path $HOME ".cursor"; break }
        "droid" { Join-Path $HOME ".factory"; break }
        "gemini-cli" { Join-Path $HOME ".gemini"; break }
        "github-copilot" { Join-Path $HOME ".copilot"; break }
        "goose" { Join-Path $HOME ".config\goose"; break }
        "iflow-cli" { Join-Path $HOME ".iflow"; break }
        "junie" { Join-Path $HOME ".junie"; break }
        "kilo" { Join-Path $HOME ".kilocode"; break }
        "kiro-cli" { Join-Path $HOME ".kiro"; break }
        "kode" { Join-Path $HOME ".kode"; break }
        "mcpjam" { Join-Path $HOME ".mcpjam"; break }
        "mistral-vibe" { Join-Path $HOME ".vibe"; break }
        "mux" { Join-Path $HOME ".mux"; break }
        "neovate" { Join-Path $HOME ".neovate"; break }
        "openclaw" { Join-Path $HOME ".openclaw"; break }
        "opencode" { Join-Path $HOME ".config\opencode"; break }
        "openhands" { Join-Path $HOME ".openhands"; break }
        "pi" { Join-Path $HOME ".pi"; break }
        "pochi" { Join-Path $HOME ".pochi"; break }
        "qoder" { Join-Path $HOME ".qoder"; break }
        "qwen-code" { Join-Path $HOME ".qwen"; break }
        "roo" { Join-Path $HOME ".roo"; break }
        "trae" { Join-Path $HOME ".trae"; break }
        "trae-cn" { Join-Path $HOME ".trae-cn"; break }
        "windsurf" { Join-Path $HOME ".codeium\windsurf"; break }
        "zencoder" { Join-Path $HOME ".zencoder"; break }
        default { throw "Unsupported agent id: $Id" }
    }
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

        $line = Get-Content $sums | Where-Object { $_ -match "\s$asset$" } | Select-Object -First 1
        if (-not $line) {
            throw "$asset is missing from SHA256SUMS"
        }

        $expected = $line.Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)[0]
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

$selectedAgents = @()
foreach ($id in $Agent) {
    $selectedAgents += Normalize-AgentId $id
}
if ($Codex) {
    $selectedAgents += "codex"
}
if ($Claude) {
    $selectedAgents += "claude-code"
}
if ($All -or $AllAgents) {
    $selectedAgents = $AgentIds
}
elseif ($Detected) {
    $selectedAgents = @()
    foreach ($id in $AgentIds) {
        if (Test-Path (Get-AgentConfigDir $id)) {
            $selectedAgents += $id
        }
    }
}
elseif ($selectedAgents.Count -eq 0) {
    $selectedAgents = @("codex", "claude-code")
}

$destinations = [ordered]@{}
foreach ($id in $selectedAgents) {
    $normalized = Normalize-AgentId $id
    if ($AgentIds -notcontains $normalized) {
        throw "Unsupported agent id: $id"
    }
    $dest = Get-AgentSkillDir $normalized
    if (-not $destinations.Contains($dest)) {
        $destinations[$dest] = $true
    }
}

$tag = $null
if (-not $Source -or -not $NoBinary) {
    $tag = Resolve-Tag
}
elseif ($Source -and -not (Test-Path $Source)) {
    throw "Source path does not exist: $Source"
}

foreach ($dest in $destinations.Keys) {
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
Write-Host "Done. Restart any agent that should discover this skill for the first time."
