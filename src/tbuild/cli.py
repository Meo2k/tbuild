import os
import sys
import json
import shutil
import re
import platform
import subprocess
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"
CONFIG_FILE = Path(__file__).parent / "templates.json"

# Colors
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
RED = "\033[0;31m"
BOLD = "\033[1m"
NC = "\033[0m"

def get_current_os() -> str:
    """Detect current operating system key (linux, windows, darwin)."""
    sys_name = platform.system().lower()
    if sys_name == "linux":
        return "linux"
    elif sys_name == "windows":
        return "windows"
    elif sys_name in ("darwin", "macos"):
        return "darwin"
    return sys_name

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"{YELLOW}⚠ Warning:{NC} Failed to load templates.json: {e}")
    return {}

def resolve_language(language_raw: str, config: dict) -> tuple[str, dict]:
    lang_key = language_raw.lower()
    for name, info in config.items():
        if lang_key == name or lang_key in info.get("aliases", []):
            return name, info
    return None, None

def replace_in_file(filepath: Path, substitutions: dict):
    """Replace placeholder strings in a text file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        for key, value in substitutions.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"{{{key}}}", str(value))
        filepath.write_text(content, encoding="utf-8")
    except UnicodeDecodeError:
        pass  # Skip binary files

def process_os_folder(target_dir: Path, current_os: str):
    """If target_dir contains an 'os' folder, copy current OS files to target_dir root, then delete 'os'."""
    os_dir = target_dir / "os"
    if not os_dir.exists() or not os_dir.is_dir():
        return
        
    print(f"  {CYAN}→{NC} Detected OS: '{current_os}'. Processing os/ directory...")
    
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
        print(f"  {GREEN}✓{NC} Extracted OS files from os/{os_target_subdir.name}/ to project root")
    else:
        print(f"  {YELLOW}⚠{NC} No specific files found under os/{current_os}/")
        
    # Remove the entire 'os' folder from generated project
    shutil.rmtree(os_dir, ignore_errors=True)

def scaffold_project(language_raw: str, project_name: str):
    config = load_config()
    template_lang, lang_info = resolve_language(language_raw, config)
    
    if not template_lang:
        supported = list(config.keys())
        print(f"{RED}✗ Error:{NC} Unsupported language '{language_raw}'.")
        print(f"  Supported templates in templates.json: {', '.join(supported)}")
        sys.exit(1)
        
    template_dir = TEMPLATES_DIR / template_lang
    if not template_dir.exists():
        print(f"{RED}✗ Error:{NC} Template directory not found at '{template_dir}'.")
        sys.exit(1)
        
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", project_name):
        print(f"{RED}✗ Error:{NC} Invalid project name '{project_name}'.")
        print("  Must start with a letter/underscore and contain only letters, digits, _ or -")
        sys.exit(1)
        
    target_dir = Path.cwd() / project_name
    if target_dir.exists():
        print(f"{RED}✗ Error:{NC} Directory '{project_name}' already exists.")
        sys.exit(1)
        
    current_os = get_current_os()
    print(f"\n{BOLD}🚀 Creating {template_lang} project:{NC} {project_name} ({current_os})\n")
    
    # Copy template tree
    shutil.copytree(template_dir, target_dir)
    
    # Extract files from os/<current_os>/ and delete os/ folder
    process_os_folder(target_dir, current_os)
    
    # Gather placeholders from templates.json for current_os
    os_info = lang_info.get("os", {}).get(current_os, {})
    if not os_info and current_os == "darwin":
        os_info = lang_info.get("os", {}).get("macos", {})
    placeholders = os_info.get("placeholders", {})
    
    substitutions = {
        "PROJECT_NAME": project_name,
        **placeholders
    }
    
    # Process files in target directory
    for file_path in target_dir.rglob("*"):
        if file_path.is_file():
            # Rename gitignore.template -> .gitignore
            if file_path.name == "gitignore.template":
                new_path = file_path.parent / ".gitignore"
                file_path.rename(new_path)
                file_path = new_path
                
            # Perform text replacement
            replace_in_file(file_path, substitutions)
            
            # Chmod +x for shell scripts on POSIX
            if file_path.suffix == ".sh" and os.name == "posix":
                file_path.chmod(file_path.stat().st_mode | 0o755)
                
    # Execute post_init commands specified in templates.json using Python
    post_commands = lang_info.get("post_init", [])
    if post_commands:
        print(f"  {CYAN}→{NC} Running post-init commands from templates.json:")
        for cmd in post_commands:
            formatted_cmd = cmd.replace("{{PROJECT_NAME}}", project_name).replace("{PROJECT_NAME}", project_name)
            print(f"    • {formatted_cmd}")
            try:
                res = subprocess.run(formatted_cmd, shell=True, cwd=target_dir, capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"      {GREEN}✓{NC} Success")
                else:
                    err_msg = res.stderr.strip() or res.stdout.strip()
                    print(f"      {YELLOW}⚠{NC} Warning (code {res.returncode}): {err_msg}")
            except Exception as e:
                print(f"      {RED}✗ Error:{NC} {e}")
                
    print(f"\n{GREEN}{BOLD}✅ '{project_name}' ready!{NC}\n")
    print(f"{BOLD}Next steps:{NC}")
    print(f"  cd {project_name}")
    if template_lang == "python":
        print("  uv run src/main.py")
    else:
        req_cmd = placeholders.get("REQUIREMENTS_CMD", "./requirements.sh install")
        build_cmd = placeholders.get("BUILD_CMD", "./build.sh")
        print(f"  {req_cmd}    # (optional) install dependencies")
        print(f"  {build_cmd}                   # build & run")

def main():
    args = sys.argv[1:]
    config = load_config()
    
    if not args or "--help" in args or "-h" in args:
        print(f"{BOLD}tbuild{NC} — Cross-platform project scaffolding tool\n")
        print(f"{BOLD}Usage:{NC}")
        print("  tbuild init <language> <project_name>\n")
        print(f"{BOLD}Supported Languages (from templates.json):{NC}")
        for name, info in config.items():
            aliases = f" ({', '.join(info['aliases'])})" if info.get("aliases") else ""
            desc = info.get("description", "")
            print(f"  {name:<12}{aliases:<10} {desc}")
        print(f"\n{BOLD}Examples:{NC}")
        print("  tbuild init python my_py_app")
        print("  tbuild init cpp my_cpp_app")
        print("  tbuild init c my_c_lib")
        sys.exit(0)
        
    if len(args) < 3 or args[0] != "init":
        print(f"{RED}✗ Error:{NC} Invalid usage. Expected syntax: tbuild init <language> <project_name>")
        sys.exit(1)
        
    language = args[1]
    project_name = args[2]
    scaffold_project(language, project_name)

if __name__ == "__main__":
    main()
