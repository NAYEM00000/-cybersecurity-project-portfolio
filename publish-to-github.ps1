$ErrorActionPreference = "Stop"
$repoUrl = "https://github.com/NAYEM00000/-cybersecurity-project-portfolio.git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Install Git for Windows from https://git-scm.com/download/win and run this script again."
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".git")) {
    git init
}
git branch -M main

$existing = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

git add .
git commit -m "Publish cybersecurity project portfolio"
if ($LASTEXITCODE -ne 0) {
    Write-Host "No new changes to commit, or Git needs your user.name/user.email configuration."
    Write-Host 'Configure with: git config --global user.name "Your Name"'
    Write-Host 'And: git config --global user.email "you@example.com"'
    Read-Host "Press Enter to exit"
    exit 1
}

git push -u origin main
Write-Host "Portfolio pushed. Open: https://github.com/NAYEM00000/-cybersecurity-project-portfolio"
Read-Host "Press Enter to exit"
