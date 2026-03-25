# Script PowerShell para fazer commit e push das melhorias para o GitHub
# Uso: .\commit_and_push.ps1 -Message "mensagem do commit"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

Write-Host "🚀 Iniciando processo de commit e push..." -ForegroundColor Green
Write-Host "📝 Mensagem do commit: $Message" -ForegroundColor Cyan
Write-Host ""

# Adiciona todos os arquivos modificados
Write-Host "📦 Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Verifica se há mudanças para commit
$changes = git diff --cached --name-only
if (-not $changes) {
    Write-Host "✅ Nenhuma mudança para commit" -ForegroundColor Green
    exit 0
}

# Mostra os arquivos que serão commitados
Write-Host ""
Write-Host "📋 Arquivos que serão commitados:" -ForegroundColor Cyan
git diff --cached --name-only | ForEach-Object { Write-Host "   - $_" -ForegroundColor White }
Write-Host ""

# Faz o commit
Write-Host "💾 Fazendo commit..." -ForegroundColor Yellow
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao fazer commit" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Commit realizado com sucesso!" -ForegroundColor Green
Write-Host ""

# Mostra o status do repositório
Write-Host "📊 Status do repositório:" -ForegroundColor Cyan
git status
Write-Host ""

# Pergunta se deseja fazer push
$response = Read-Host "Deseja fazer push para o GitHub? (s/n)" 

if ($response -eq "s" -or $response -eq "S") {
    Write-Host "📤 Fazendo push para o GitHub..." -ForegroundColor Yellow
    git push origin main

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erro ao fazer push" -ForegroundColor Red
        exit 1
    }

    Write-Host "✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Melhorias enviadas para o GitHub!" -ForegroundColor Green
    Write-Host "🔗 Repositório: https://github.com/Ronbragaglia/Assistente_simples" -ForegroundColor Cyan
} else {
    Write-Host "ℹ️  Push não realizado. Você pode fazer manualmente com:" -ForegroundColor Yellow
    Write-Host "   git push origin main" -ForegroundColor White
}
