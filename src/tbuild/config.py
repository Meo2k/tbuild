import json
from pathlib import Path
from tbuild.ui import print_warning

PACKAGE_ROOT = Path(__file__).parent
TEMPLATES_DIR = PACKAGE_ROOT / "templates"
CONFIG_FILE = PACKAGE_ROOT / "templates.json"

def load_config() -> dict:
    """Load configuration from templates.json."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print_warning(f"Failed to load templates.json: {e}")
    return {}

def resolve_language(language_raw: str, config: dict) -> tuple[str | None, dict | None]:
    """Resolve language name and its configuration using raw input and aliases."""
    lang_key = language_raw.lower()
    for name, info in config.items():
        if lang_key == name or lang_key in info.get("aliases", []):
            return name, info
    return None, None
