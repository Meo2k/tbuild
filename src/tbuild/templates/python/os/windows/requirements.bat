@echo off
setlocal enabledelayedexpansion

set "ACTION=%~1"

if /i "%ACTION%"=="install" (
    echo [1/2] Checking Python...
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        echo Python is already installed.
    ) else (
        echo Installing Python...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
        ) else (
            where choco >nul 2>&1
            if !errorlevel! equ 0 (
                choco install python3 -y
            ) else (
                echo Neither winget nor choco found. Please install Python manually.
            )
        )
    )

    echo [2/2] Checking uv...
    where uv >nul 2>&1
    if !errorlevel! equ 0 (
        echo uv is already installed.
    ) else (
        echo Installing uv...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id astral-sh.uv --accept-source-agreements --accept-package-agreements
        ) else (
            where choco >nul 2>&1
            if !errorlevel! equ 0 (
                choco install uv -y
            ) else (
                echo Installing uv via official PowerShell installer...
                powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
            )
        )
    )

    echo Reloading PATH environment variable...
    for /f "usebackq delims=" %%P in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User')"` ) do (
        set "PATH=%%P"
    )
    if exist "%USERPROFILE%\.local\bin" set "PATH=%USERPROFILE%\.local\bin;!PATH!"
    if exist "%USERPROFILE%\.cargo\bin" set "PATH=%USERPROFILE%\.cargo\bin;!PATH!"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User')" >nul 2>&1

    echo Completed dependencies installation.
    exit /b 0
)

echo Usage:
echo   requirements.bat install  -^> check and install Python and uv
exit /b 1
