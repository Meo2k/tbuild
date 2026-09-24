@echo off

where cl >nul 2>&1 || where g++ >nul 2>&1 || where clang++ >nul 2>&1 || for /f "usebackq tokens=*" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2^>nul`) do call "%%i\VC\Auxiliary\Build\vcvars64.bat"

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
if %errorlevel% neq 0 exit /b %errorlevel%
cmake --build build
if %errorlevel% neq 0 exit /b %errorlevel%

.\build\bin\Debug_Windows_AMD64\{PROJECT_NAME}.exe