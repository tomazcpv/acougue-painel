@echo off
echo ===============================
echo Atualizando painel do acougue
echo ===============================

REM 1 - Gerar produtos.json (se você usa script python)
python gerar_produtos.py

REM 2 - Atualizar version.txt com timestamp atual
for /f %%i in ('powershell -command "[int][double]::Parse((Get-Date -UFormat %%s))"') do set VERSAO=%%i
echo %VERSAO% > version.txt

echo Nova versao: %VERSAO%

REM 3 - Adicionar tudo
git add .

REM 4 - Commit automatico
git commit -m "Atualizacao automatica painel - %VERSAO%"

REM 5 - Enviar para GitHub
git push

echo ===============================
echo Painel atualizado com sucesso!
echo ===============================
pause