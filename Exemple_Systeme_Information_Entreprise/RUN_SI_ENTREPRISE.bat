@echo off
setlocal
chcp 65001 >nul
title Installation et lancement - Systeme d'information Python

echo ================================================
echo  SYSTEME D'INFORMATION - INSTALLATION ET LANCEMENT
echo ================================================
echo.

REM Se placer automatiquement dans le dossier ou se trouve ce fichier BAT.
cd /d "%~dp0"

if not exist "requirements.txt" (
    echo ERREUR : requirements.txt est introuvable.
    echo Placez ce fichier BAT a la racine du projet, a cote de requirements.txt.
    pause
    exit /b 1
)

REM Detecter Python 3.12 sans utiliser .venv.
set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    py -3.12 --version >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py -3.12"
)

if not defined PY_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python --version
        if not errorlevel 1 set "PY_CMD=python"
    )
)

if not defined PY_CMD (
    echo ERREUR : Python 3.12 est introuvable.
    echo Testez dans CMD : py -0p
    echo Ou installez Python et activez son ajout au PATH.
    pause
    exit /b 1
)

echo [1/3] Python detecte :
%PY_CMD% --version
if errorlevel 1 (
    echo ERREUR : impossible de lancer Python.
    pause
    exit /b 1
)

echo.
echo [2/3] Installation des dependances depuis requirements.txt...
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 (
    echo AVERTISSEMENT : mise a jour de pip echouee. Tentative d'installation continuee...
)
%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERREUR : installation des dependances echouee.
    echo Verifiez votre connexion Internet et le fichier requirements.txt.
    pause
    exit /b 1
)

echo.
echo [3/3] Demarrage du serveur...
echo Application : http://127.0.0.1:8000
echo Documentation API : http://127.0.0.1:8000/docs
echo.
echo Gardez cette fenetre ouverte pendant le test.
echo Pour arreter le serveur, appuyez sur Ctrl+C.
echo.

%PY_CMD% -m uvicorn backend.main:app --reload
echo.
echo Le serveur est arrete.
pause
endlocal