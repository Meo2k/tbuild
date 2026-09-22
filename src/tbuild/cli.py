import sys

from tbuild.config import load_config
from tbuild.scaffolder import scaffold_project
from tbuild.ui import print_error, print_help

def main() -> None:
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        config = load_config()
        print_help(config)
        sys.exit(0)

    if len(args) < 3 or args[0] != "init":
        print_error("Invalid usage. Expected syntax: tbuild init <language> <project_name>")
        sys.exit(1)

    language = args[1]
    project_name = args[2]

    success = scaffold_project(language, project_name)
    if not success:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
