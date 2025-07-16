@echo off
title Systeme de Paiement NeoBot Premium
color 0A

echo ========================================
echo    SYSTEME DE PAIEMENT NEOBOT PREMIUM
echo ========================================
echo.

echo [1/4] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo [2/4] Installation des dependances...
pip install -r requirements_premium.txt
if errorlevel 1 (
    echo ERREUR: Echec de l'installation des dependances
    pause
    exit /b 1
)

echo [3/4] Verification de la configuration...
if not exist "premium_config.json" (
    echo ERREUR: Fichier premium_config.json manquant
    echo Veuillez configurer le fichier premium_config.json
    pause
    exit /b 1
)

echo [4/4] Demarrage du serveur web...
echo.
echo ========================================
echo    SERVEUR ACCESSIBLE SUR:
echo    http://localhost:5000
echo ========================================
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python premium_system.py

pause 