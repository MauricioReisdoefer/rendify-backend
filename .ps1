Clear-Host

py -m pytest

# Verificar se o pytest retornou sucesso
if ($LASTEXITCODE -eq 0) {
    Clear-Host
    Write-Host "----------------------------------"
    Write-Host "Todos os testes passaram!"
    Write-Host "----------------------------------"

    # Pedir mensagem do commit
    $commitMessage = Read-Host "Digite a mensagem do commit"

    # Fazer commit
    git add .
    git commit -m "$commitMessage"
    git push origin main

    Clear-Host
    Write-Host "----------------------------------"
    Write-Host "Commit criado com sucesso!"
    Write-Host "----------------------------------"
}
else {
    Write-Host "----------------------------------"
    Write-Host "Testes falharam. Commit cancelado."
    Write-Host "----------------------------------"
}
