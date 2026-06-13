@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Image Data Extract Python - Windows Installer
:: Developer: issu321
:: GitHub: https://github.com/issu321
:: Repository: https://github.com/issu321/Image-Data-Extract-Python
:: ============================================================

:: =========================
:: COLORS
:: =========================
set "RED=\033[0;31m"
set "GREEN=\033[0;32m"
set "YELLOW=\033[1;33m"
set "BLUE=\033[0;34m"
set "CYAN=\033[0;36m"
set "MAGENTA=\033[0;35m"
set "NC=\033[0m"

:: Enable ANSI colors on Windows 10+
reg query "HKCU\Console" /v VirtualTerminalLevel >nul 2>&1
if %errorlevel% neq 0 (
    reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
)

cls

:: =========================
:: TYPEWRITER EFFECT
:: =========================
call :typewriter "[SYSTEM] Initializing OCR core modules..." 20
ping -n 1 -w 300 127.0.0.1 >nul
echo.
call :typewriter "[KERNEL] Loading image processing protocols..." 20
ping -n 1 -w 300 127.0.0.1 >nul
echo.
call :typewriter "[DAEMON] Mounting Tesseract OCR engine..." 20
ping -n 1 -w 300 127.0.0.1 >nul
echo.
call :typewriter "[SECURE] Handshake with github.com/issu321 ..." 20
ping -n 1 -w 400 127.0.0.1 >nul
echo.
cls

:: =========================
:: HEADER
:: =========================
call :color 36
call :typewriter "============================================================" 3
echo.
call :typewriter "    IMAGE DATA EXTRACT PYTHON - WINDOWS INSTALLER" 3
echo.
call :typewriter "    AI-Powered OCR for Handwritten && Printed Text" 3
echo.
call :typewriter "    github.com/issu321" 3
echo.
call :typewriter "    github.com/issu321/Image-Data-Extract-Python" 3
echo.
call :typewriter "============================================================" 3
echo.
call :color 0

call :color 35
echo.
echo  ============================================================
echo   Image Data Extract Python
echo   Developed by issu321
echo  ============================================================
echo.
call :color 0

:: =========================
:: PYTHON CHECK
:: =========================
call :color 32
call :typewriter "[SCAN] Detecting Python environment..." 20
echo.
call :color 0

python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        call :color 31
        echo [ERROR] Python not found.
        echo Please install Python 3.11+ from https://python.org
        call :color 0
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)

for /f "tokens=2" %%a in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%a"

echo.
call :color 32
echo [OK] Python : %PYTHON_VERSION%
call :color 0
echo.

:: =========================
:: VENV NOTICE
:: =========================
call :color 33
call :typewriter "[ALERT] Virtual Environment Recommended" 20
echo.
call :color 0

call :color 33
echo.
echo  ============================================================
echo   IMPORTANT NOTICE
echo  ============================================================
echo.
echo  Using a Python Virtual Environment is VERY IMPORTANT
echo  and HIGHLY RECOMMENDED.
echo.
echo  Why? Because it keeps your project dependencies isolated
echo  from your system Python packages. This prevents version
echo  conflicts, keeps your system clean, and makes your app
echo  portable and easy to deploy.
echo.
echo  Without a virtual environment, packages may conflict with
echo  other projects or system tools, causing crashes and broken
echo  installations.
echo.
echo  Follow these steps to create and activate a virtual environment:
echo.
echo  -----------------------------------------
echo    Step 1: Create the virtual env
echo    ^> python -m venv venv
echo.
echo    Step 2: Activate the virtual env
echo    ^> venv\Scripts\activate
echo.
echo    Step 3: Run the installer
echo    ^> install.bat
echo.
echo    Step 4: Deactivate when done
echo    ^> deactivate
echo  -----------------------------------------
echo.
call :color 0

call :color 36
call :typewriter ">>> Type yes  -^> Continue (venv created)" 20
echo.
call :typewriter ">>> Type no   -^> Continue (no venv)" 20
echo.
call :typewriter ">>> Type exit -^> Stop installer" 20
echo.
call :color 0

echo.
set /p USER_INPUT="Enter choice (yes/no/exit): "

if /i "%USER_INPUT%"=="exit" (
    echo.
    call :color 31
    call :typewriter "[ABORT] Installer terminated by user." 20
    echo.
    call :color 0
    pause
    exit /b 1
)

if /i not "%USER_INPUT%"=="yes" if /i not "%USER_INPUT%"=="no" (
    echo.
    call :color 31
    call :typewriter "[ERROR] Invalid input." 20
    echo.
    call :color 0
    pause
    exit /b 1
)

if /i "%USER_INPUT%"=="yes" (
    echo.
    call :color 32
    call :typewriter "[ACCESS GRANTED] Proceeding with venv installation..." 20
    echo.
    call :color 0
) else (
    echo.
    call :color 33
    call :typewriter "[WARNING] Proceeding without virtual environment..." 20
    echo.
    call :color 0
)

echo.

:: =========================
:: INSTALLATION STEPS
:: =========================
if /i "%USER_INPUT%"=="yes" (
    call :color 34
    call :typewriter "[1/4] Creating virtual environment..." 20
    echo.
    call :color 0

    %PYTHON_CMD% -m venv venv

    echo.
    call :color 34
    call :typewriter "[2/4] Activating virtual environment..." 20
    echo.
    call :color 0

    call venv\Scripts\activate.bat

    echo.
    call :color 34
    call :typewriter "[3/4] Installing dependencies..." 20
    echo.
    call :color 0

    pip install -r requirements.txt

    echo.
    call :color 34
    call :typewriter "[4/4] Finalizing installation..." 20
    echo.
    call :color 0
) else (
    call :color 34
    call :typewriter "[1/2] Installing dependencies..." 20
    echo.
    call :color 0

    %PYTHON_CMD% -m pip install -r requirements.txt

    echo.
    call :color 34
    call :typewriter "[2/2] Finalizing installation..." 20
    echo.
    call :color 0
)

:: =========================
:: COMPLETE
:: =========================
echo.
call :color 32
call :typewriter "============================================================" 3
echo.
call :typewriter "              INSTALLATION COMPLETE" 3
echo.
call :typewriter "============================================================" 3
echo.
call :color 0

echo.
call :color 32
call :typewriter "[SUCCESS] Dependencies Installed" 20
echo.
call :typewriter "[SUCCESS] Image Data Extract Python Ready" 20
echo.
call :color 0

echo.
call :color 36
call :typewriter "To start the app:" 20
echo.
call :typewriter "  venv\Scripts\activate" 20
echo.
call :typewriter "  python app.py" 20
echo.
call :typewriter "Then open the URL shown in your terminal" 20
echo.
call :color 0

echo.
echo  Developer : issu321
echo  GitHub    : https://github.com/issu321
echo  Repository: https://github.com/issu321/Image-Data-Extract-Python
echo.

call :color 35
call :typewriter "[LAUNCH] Preparing to start Image Data Extract Python..." 20
echo.
call :color 0

echo.

call :color 33
call :typewriter "Starting in 3..." 60
echo.
ping -n 2 -w 500 127.0.0.1 >nul
call :typewriter "Starting in 2..." 60
echo.
ping -n 2 -w 500 127.0.0.1 >nul
call :typewriter "Starting in 1..." 60
echo.
ping -n 2 -w 500 127.0.0.1 >nul
call :color 0

echo.
call :color 32
call :typewriter "[LAUNCH] Starting Application..." 20
echo.
call :color 0
echo.

if /i "%USER_INPUT%"=="yes" (
    call venv\Scripts\activate.bat
    python app.py
) else (
    %PYTHON_CMD% app.py
)

pause
exit /b 0

:: =========================
:: FUNCTIONS
:: =========================
:typewriter
set "text=%~1"
set "delay=%~2"
if "%delay%"=="" set "delay=30"
for /l %%i in (0,1,255) do (
    set "char=!text:~%%i,1!"
    if "!char!"=="" goto :eof
    <nul set /p "=!char!"
    ping -n 1 -w %delay% 127.0.0.1 >nul
)
goto :eof

:color
powershell -Command "$host.ui.RawUI.ForegroundColor = '%~1'" >nul 2>&1
if %errorlevel% neq 0 (
    :: Fallback for older Windows without PowerShell color support
)
goto :eof
