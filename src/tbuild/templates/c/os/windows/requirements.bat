@echo off
set ACTION=%1

if "%ACTION%"=="update" (
    if exist build\compile_commands.json (
        copy /y build\compile_commands.json compile_commands.json
        echo compile_commands.json updated.
    ) else (
        echo compile_commands.json not found in build directory. Please run build.bat first.
    )
) else (
    echo Usage:
    echo   requirements.bat update   -^> copy compile_commands.json for editor
)
