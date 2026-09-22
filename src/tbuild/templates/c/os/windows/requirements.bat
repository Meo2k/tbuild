@echo off
setlocal enabledelayedexpansion

set "ACTION=%~1"

if /i "%ACTION%"=="install" (
    echo [1/3] Checking Ninja...
    where ninja >nul 2>&1
    if !errorlevel! equ 0 (
        echo ninja is already installed.
    ) else (
        echo Installing ninja...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Ninja-build.Ninja --accept-source-agreements --accept-package-agreements
        ) else (
            where choco >nul 2>&1
            if !errorlevel! equ 0 (
                choco install ninja -y
            ) else (
                echo Neither winget nor choco found. Please install ninja manually.
            )
        )
    )

    echo [2/3] Checking CMake...
    where cmake >nul 2>&1
    if !errorlevel! equ 0 (
        echo cmake is already installed.
    ) else (
        echo Installing cmake...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Kitware.CMake --accept-source-agreements --accept-package-agreements
        ) else (
            where choco >nul 2>&1
            if !errorlevel! equ 0 (
                choco install cmake -y
            ) else (
                echo Neither winget nor choco found. Please install cmake manually.
            )
        )
    )

    echo [3/3] Checking C Build Tools...
    set "HAS_COMPILER=0"
    where cl >nul 2>&1 && set "HAS_COMPILER=1"
    where gcc >nul 2>&1 && set "HAS_COMPILER=1"
    where clang >nul 2>&1 && set "HAS_COMPILER=1"
    if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" (
        for /f "usebackq tokens=*" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2^>nul`) do (
            if not "%%i"=="" set "HAS_COMPILER=1"
        )
    )
    if !HAS_COMPILER! equ 1 (
        echo C compiler / Visual Studio Build Tools is already installed.
    ) else (
        echo Installing Visual Studio Build Tools...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended" --accept-source-agreements --accept-package-agreements
        ) else (
            echo winget not found. Please install Visual Studio Build Tools manually.
        )
    )

    echo Reloading PATH environment variable...
    for /f "usebackq delims=" %%P in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User')"` ) do (
        set "PATH=%%P"
    )
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User')" >nul 2>&1

    echo Completed dependencies installation.
    exit /b 0
)

if /i "%ACTION%"=="update" (
    if exist "build\compile_commands.json" (
        if exist "compile_commands.json" del /f /q "compile_commands.json"
        
        mklink "compile_commands.json" "build\compile_commands.json" >nul
        if !errorlevel! equ 0 (
            echo compile_commands.json linked successfully.
        ) else (
            echo Failed to create symlink. Try running CMD as Administrator or enable Developer Mode.
        )
    ) else (
        echo Not found compile_commands.json file in build directory. Please run build script first.
    )
    exit /b 0
)

echo Usage:
echo   requirements.bat install  -^> install ninja, cmake, and C build tools
echo   requirements.bat update   -^> create symlink for compile_commands.json
exit /b 1
