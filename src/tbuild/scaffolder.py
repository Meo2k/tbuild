import os
import re
import shutil
import subprocess
from pathlib import Path

from tbuild.config import TEMPLATES_DIR, load_config, resolve_language
from tbuild.platform_utils import get_current_os
from tbuild.ui import (
    print_bullet,
    print_completed,
    print_error,
    print_header,
    print_step,
    print_substep_error,
    print_substep_success,
    print_substep_warning,
    print_success,
    print_warning,
)

def replace_in_file(filepath: Path, substitutions: dict) -> None:
    """Replace placeholder strings in a text file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        for key, value in substitutions.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"{{{key}}}", str(value))
        filepath.write_text(content, encoding="utf-8")
    except UnicodeDecodeError:
        pass  # Skip binary files

def process_os_folder(target_dir: Path, current_os: str) -> None:
    """If target_dir contains an 'os' folder, copy current OS files to target_dir root, then delete 'os'."""
    os_dir = target_dir / "os"
    if not os_dir.exists() or not os_dir.is_dir():
        return

    print_step(f"Detected OS: '{current_os}'. Processing os/ directory...")

    # Check for matching OS folder (support darwin/macos alias)
    os_target_subdir = os_dir / current_os
    if not os_target_subdir.exists() and current_os in ("darwin", "macos"):
        os_target_subdir = os_dir / "macos" if (os_dir / "macos").exists() else os_dir / "darwin"

    if os_target_subdir.exists() and os_target_subdir.is_dir():
        for item in os_target_subdir.iterdir():
            dest = target_dir / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        print_success(f"Extracted OS files from os/{os_target_subdir.name}/ to project root")
    else:
        print_warning(f"No specific files found under os/{current_os}/")

    # Remove the entire 'os' folder from generated project
    shutil.rmtree(os_dir, ignore_errors=True)

def execute_post_init(post_commands: list[str], target_dir: Path, project_name: str) -> None:
    """Execute post_init shell commands for the generated project."""
    if not post_commands:
        return

    print_step("Running post-init commands from templates.json:")
    for cmd in post_commands:
        formatted_cmd = cmd.replace("{{PROJECT_NAME}}", project_name).replace("{PROJECT_NAME}", project_name)
        print_bullet(formatted_cmd)
        try:
            res = subprocess.run(formatted_cmd, shell=True, cwd=target_dir, capture_output=True, text=True)
            if res.returncode == 0:
                print_substep_success("Success")
            else:
                err_msg = res.stderr.strip() or res.stdout.strip()
                print_substep_warning(res.returncode, err_msg)
        except Exception as e:
            print_substep_error(str(e))

def scaffold_project(language_raw: str, project_name: str) -> bool:
    """Core workflow for scaffolding a project from templates."""
    config = load_config()
    template_lang, lang_info = resolve_language(language_raw, config)

    if not template_lang:
        supported = list(config.keys())
        print_error(f"Unsupported language '{language_raw}'.")
        print_step(f"Supported templates in templates.json: {', '.join(supported)}")
        return False

    template_dir = TEMPLATES_DIR / template_lang
    if not template_dir.exists():
        print_error(f"Template directory not found at '{template_dir}'.")
        return False

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", project_name):
        print_error(f"Invalid project name '{project_name}'.")
        print_step("Must start with a letter/underscore and contain only letters, digits, _ or -")
        return False

    target_dir = Path.cwd() / project_name
    if target_dir.exists():
        print_error(f"Directory '{project_name}' already exists.")
        return False

    current_os = get_current_os()
    print_header(template_lang, project_name, current_os)

    # 1. Copy template files
    shutil.copytree(template_dir, target_dir)

    # 2. Extract OS-specific files
    process_os_folder(target_dir, current_os)

    # 3. Gather placeholders from templates.json for current_os
    os_info = lang_info.get("os", {}).get(current_os, {})
    if not os_info and current_os == "darwin":
        os_info = lang_info.get("os", {}).get("macos", {})
    placeholders = os_info.get("placeholders", {})

    substitutions = {
        "PROJECT_NAME": project_name,
        **placeholders,
    }

    # 4. Process files in target directory (rename gitignore, substitute variables, set chmod)
    for file_path in target_dir.rglob("*"):
        if file_path.is_file():
            if file_path.name == "gitignore.template":
                new_path = file_path.parent / ".gitignore"
                file_path.rename(new_path)
                file_path = new_path

            replace_in_file(file_path, substitutions)

            if file_path.suffix == ".sh" and os.name == "posix":
                file_path.chmod(file_path.stat().st_mode | 0o755)

    # 5. Execute post-init commands
    post_commands = lang_info.get("post_init", [])
    execute_post_init(post_commands, target_dir, project_name)

    # 6. Show next steps
    print_completed(project_name, template_lang, placeholders)
    return True
