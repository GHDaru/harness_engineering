<#
.SYNOPSIS
  Sincroniza localmente todos os forks do projeto Engenharia de Harness com seus upstreams.

.DESCRIPTION
  Para cada repositório da lista:
    1. Clona o fork (GHDaru/<repo>) se ainda não existir em -BaseDir;
    2. Garante o remote 'upstream' apontando para o repositório original;
    3. Busca o upstream e detecta a branch default;
    4. Faz merge fast-forward-only da branch default do upstream;
    5. Empurra o resultado para o fork (origin).
  O merge é --ff-only de propósito: se você tiver commits locais divergentes,
  o script AVISA e não sobrescreve nada — resolva manualmente (rebase) e rode de novo.

  O repositório do livro (harness_engineering) não tem upstream: para ele o script
  apenas faz pull --ff-only do próprio origin.

.PARAMETER BaseDir
  Diretório onde os clones vivem (default: ~\harness-repos).

.PARAMETER Only
  Sincroniza apenas os repositórios nomeados (ex.: -Only goose,aider).

.PARAMETER NoPush
  Atualiza os clones locais mas não empurra para os forks no GitHub.

.EXAMPLE
  .\sync-forks.ps1
  .\sync-forks.ps1 -BaseDir D:\repos -Only langgraph,crewAI
  .\sync-forks.ps1 -NoPush
#>
[CmdletBinding()]
param(
    [string]$BaseDir = (Join-Path $HOME 'harness-repos'),
    [string[]]$Only = @(),
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'
$ForkOwner = 'GHDaru'

# name = nome do fork em GHDaru/<name>; upstream = owner/repo original ($null = sem upstream)
$Repos = @(
    @{ name = 'harness_engineering';   upstream = $null }
    # Harnesses de código
    @{ name = 'opencode';              upstream = 'anomalyco/opencode' }
    @{ name = 'gemini-cli';            upstream = 'google-gemini/gemini-cli' }
    @{ name = 'OpenHarness';           upstream = 'HKUDS/OpenHarness' }
    @{ name = 'codex';                 upstream = 'openai/codex' }
    @{ name = 'goose';                 upstream = 'block/goose' }
    @{ name = 'aider';                 upstream = 'Aider-AI/aider' }
    @{ name = 'OpenHands';             upstream = 'All-Hands-AI/OpenHands' }
    @{ name = 'software-agent-sdk';    upstream = 'OpenHands/software-agent-sdk' }
    # Agentes pessoais
    @{ name = 'openclaw';              upstream = 'openclaw/openclaw' }
    @{ name = 'hermes-agent';          upstream = 'NousResearch/hermes-agent' }
    @{ name = 'ironclaw';              upstream = 'nearai/ironclaw' }
    # Harness embutido
    @{ name = 'n8n';                   upstream = 'n8n-io/n8n' }
    # Frameworks
    @{ name = 'langgraph';             upstream = 'langchain-ai/langgraph' }
    @{ name = 'openai-agents-python';  upstream = 'openai/openai-agents-python' }
    @{ name = 'crewAI';                upstream = 'crewAIInc/crewAI' }
    # Referencial teórico
    @{ name = 'awesome-harness-engineering'; upstream = 'ai-boost/awesome-harness-engineering' }
)

function Get-DefaultBranch([string]$Dir, [string]$Remote) {
    $head = git -C $Dir symbolic-ref --quiet "refs/remotes/$Remote/HEAD" 2>$null
    if ($head) { return ($head -replace "^refs/remotes/$Remote/", '') }
    foreach ($b in @('main', 'master')) {
        git -C $Dir show-ref --verify --quiet "refs/remotes/$Remote/$b" 2>$null
        if ($LASTEXITCODE -eq 0) { return $b }
    }
    return $null
}

if (-not (Test-Path $BaseDir)) { New-Item -ItemType Directory -Path $BaseDir | Out-Null }
$results = @()

foreach ($repo in $Repos) {
    $name = $repo.name
    if ($Only.Count -gt 0 -and $Only -notcontains $name) { continue }

    $dir = Join-Path $BaseDir $name
    $forkUrl = "https://github.com/$ForkOwner/$name.git"
    Write-Host "`n=== $name ===" -ForegroundColor Cyan

    try {
        if (-not (Test-Path (Join-Path $dir '.git'))) {
            Write-Host "Clonando $forkUrl ..."
            git clone $forkUrl $dir
            if ($LASTEXITCODE -ne 0) { throw "clone falhou" }
        }

        if (-not $repo.upstream) {
            git -C $dir pull --ff-only origin
            if ($LASTEXITCODE -ne 0) { throw "pull do origin falhou (commits locais divergentes?)" }
            $results += [pscustomobject]@{ Repo = $name; Status = 'OK (origin pull)' }
            continue
        }

        $upstreamUrl = "https://github.com/$($repo.upstream).git"
        $existing = git -C $dir remote get-url upstream 2>$null
        if (-not $existing) {
            git -C $dir remote add upstream $upstreamUrl
        } elseif ($existing -ne $upstreamUrl) {
            git -C $dir remote set-url upstream $upstreamUrl
        }

        git -C $dir fetch upstream --prune
        if ($LASTEXITCODE -ne 0) { throw "fetch do upstream falhou" }
        git -C $dir remote set-head upstream --auto 2>$null | Out-Null

        $branch = Get-DefaultBranch $dir 'upstream'
        if (-not $branch) { throw "não foi possível detectar a branch default do upstream" }

        git -C $dir checkout $branch 2>$null
        if ($LASTEXITCODE -ne 0) { git -C $dir checkout -b $branch "upstream/$branch"; if ($LASTEXITCODE -ne 0) { throw "checkout de $branch falhou" } }

        git -C $dir merge --ff-only "upstream/$branch"
        if ($LASTEXITCODE -ne 0) {
            throw "merge --ff-only falhou: há commits locais em '$branch' que divergem do upstream. Resolva manualmente (ex.: git rebase upstream/$branch) e rode de novo."
        }

        if ($NoPush) {
            $results += [pscustomobject]@{ Repo = $name; Status = "OK local ($branch, sem push)" }
        } else {
            git -C $dir push origin $branch
            if ($LASTEXITCODE -ne 0) { throw "push para o fork falhou" }
            $results += [pscustomobject]@{ Repo = $name; Status = "OK ($branch sincronizada)" }
        }
    }
    catch {
        Write-Warning "[$name] $($_.Exception.Message)"
        $results += [pscustomobject]@{ Repo = $name; Status = "FALHOU: $($_.Exception.Message)" }
    }
}

Write-Host "`n========== RESUMO ==========" -ForegroundColor Green
$results | Format-Table -AutoSize
