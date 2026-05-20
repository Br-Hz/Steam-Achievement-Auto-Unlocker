@echo off
title Steam Achievement Analyzer
cd /d "%~dp0"

:: Tentar python no PATH primeiro; senao usar caminho direto
where python >nul 2>&1
if not errorlevel 1 (
    set PYTHON=python
) else (
    set PYTHON=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
)

:: Verificar Python
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado.
    echo Instale em: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Instalar dependencias se necessario
"%PYTHON%" -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    "%PYTHON%" -m pip install requests
)

:: Executar script (o Python ja exibe "Enter para sair" ao final)
"%PYTHON%" steam_achievements.py
if errorlevel 1 (
    echo.
    echo [O script terminou com erro - veja a mensagem acima]
    pause
)
