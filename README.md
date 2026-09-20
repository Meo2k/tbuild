# tbuild — Project Scaffolding Tool

`tbuild` is a cross-platform (Windows, macOS, Linux) CLI scaffolding tool to quickly generate project boilerplate templates.

## Installation with `uv`

### 1. Direct Global Install (Without cloning)

Install `tbuild` directly from remote Git repository into your system environment:

```bash
uv tool install git+https://gitlab.com/public-lovecat/tbuild.git
```

*Or run directly without installing:*

```bash
uvx --from git+https://gitlab.com/public-lovecat/tbuild.git tbuild init python my_app
```

### 2. Local Development Install

If you have cloned the repository locally and want to develop or add templates:

```bash
uv tool install --editable .
```

*After installation, the `tbuild` command will be globally available in your terminal / CMD / PowerShell.*

## Usage

```bash
tbuild init <language> <project_name>
```

### Supported Templates:
* `python` (or `py`): Initialize a Python project with `uv` and `pyproject.toml`.
* `cpp` (or `c++`): Initialize a C++20 project with CMake, Ninja, and Precompiled Headers (`pch.h`).
* `c`: Initialize a C17 project with CMake and Ninja.

### Examples:

```bash
tbuild init python my_app
tbuild init cpp my_cpp_project
tbuild init c my_c_lib
```

## Adding New Templates

To add a new project template (e.g., `rust`, `go`, `react`):
1. Create a new directory inside `src/tbuild/templates/<name>`.
2. Add your boilerplate files (use `{{PROJECT_NAME}}` as a placeholder for the project name).
3. Configure post-init setup commands, descriptions, and aliases in `src/tbuild/templates.json`.
