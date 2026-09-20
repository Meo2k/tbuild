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

---

## Configuration (`templates.json`)

All template metadata, post-initialization commands, aliases, and OS-specific placeholders are defined in `src/tbuild/templates.json`.

### Example `templates.json`:

```json
{
  "cpp": {
    "aliases": ["c++"],
    "description": "C++ project (C++20, CMake + Ninja)",
    "post_init": [
      "git init",
      "git add -A",
      "git commit -m \"chore: init cpp project via tbuild\""
    ],
    "os": {
      "linux": {
        "placeholders": {
          "REQUIREMENTS_CMD": "./requirements.sh install",
          "BUILD_CMD": "./build.sh",
          "UPDATE_CMD": "./requirements.sh update",
          "OS_NAME": "Linux"
        }
      },
      "windows": {
        "placeholders": {
          "REQUIREMENTS_CMD": "requirements.bat install",
          "BUILD_CMD": "build.bat",
          "UPDATE_CMD": "requirements.bat update",
          "OS_NAME": "Windows"
        }
      }
    }
  }
}
```

### Schema & Field Reference:

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `<template_name>` | `string` | **Yes** | Key matching the template folder name in `src/tbuild/templates/<name>`. |
| `aliases` | `list[string]` | No | Alternative command aliases for the template (e.g. `py` for `python`, `c++` for `cpp`). |
| `description` | `string` | No | Short template summary displayed in `tbuild --help`. |
| `post_init` | `list[string]` | No | List of shell commands executed sequentially inside the generated project folder. |
| `os` | `object` | No | Object containing OS-dependent configurations keyed by platform (`linux`, `windows`, `darwin`/`macos`). |
| `os.<platform>.placeholders` | `object` | No | Key-value pairs for placeholders (e.g., `{{BUILD_CMD}}` or `{BUILD_CMD}`) replaced dynamically in text files based on host OS. |

---

## Adding New Templates

To add a new template (e.g. `rust`, `go`, `react`):
1. Create a template folder in `src/tbuild/templates/<name>`.
2. *(Optional)* Add OS-specific files inside `src/tbuild/templates/<name>/os/<platform>/` (these are automatically extracted to project root and `os/` is deleted).
3. Add boilerplate files using `{{PROJECT_NAME}}` or custom placeholders.
4. Register the new template in `src/tbuild/templates.json`.
