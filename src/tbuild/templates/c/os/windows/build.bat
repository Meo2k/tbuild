@echo off
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
if %errorlevel% neq 0 exit /b %errorlevel%
cmake --build build
if %errorlevel% neq 0 exit /b %errorlevel%

.\build\bin\Debug_Windows_AMD64\{PROJECT_NAME}.exe
