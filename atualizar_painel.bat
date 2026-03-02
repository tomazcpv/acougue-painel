@echo off
setlocal

cd /d C:\acougue-painel

echo ==============================
echo Atualizando painel do açougue
echo ==============================

echo [1/4] Gerando produtos.json (filtrado)...
python gerar_produtos_json.py
if errorlevel 1 goto erro

echo [2/4] Atualizando versao do site (version.txt)...
for /f %%i in ('powershell -NoProfile -Command "[DateTimeOffset]::Now.ToUnixTimeSeconds()"') do set VERSAO=%%i
echo %VERSAO%> version.txt

echo [3/4] Commit e push no GitHub...
git add .
if errorlevel 1 goto erro

REM Commit com data/hora (evita erro "nothing to commit" caso nao haja mudanca)
for /f "tokens=1-3 delims=/" %%a in ("%date%") do set DATA=%%c-%%b-%%a
for /f "tokens=1-2 delims=:" %%a in ("%time%") do set HORA=%%a%%b

git commit -m "Atualiza painel %DATA% %HORA%" >nul 2>&1
REM Se nao tiver nada para commitar, segue mesmo assim
git push
if errorlevel 1 goto erro

echo.
echo ✅ Painel atualizado com sucesso!
echo A TV vai atualizar sozinha:
echo - Precos/itens: em ate 60s
echo - Layout/codigo: em ate 30s
echo.
pause
exit /b 0

:erro
echo.
echo ❌ Ocorreu um erro. Veja as mensagens acima.
echo.
pause
exit /b 1
