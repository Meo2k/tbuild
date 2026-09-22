from rich.console import Console

console = Console()

def print_error(msg: str) -> None:
    console.print(f"[red]✗ Error:[/red] {msg}")

def print_warning(msg: str) -> None:
    console.print(f"[yellow]⚠ Warning:[/yellow] {msg}")

def print_success(msg: str) -> None:
    console.print(f"  [green]✓[/green] {msg}")

def print_step(msg: str) -> None:
    console.print(f"  [cyan]→[/cyan] {msg}")

def print_bullet(cmd: str) -> None:
    console.print(f"    • {cmd}")

def print_substep_success(msg: str = "Success") -> None:
    console.print(f"      [green]✓[/green] {msg}")

def print_substep_warning(code: int, msg: str) -> None:
    console.print(f"      [yellow]⚠[/yellow] Warning (code {code}): {msg}")

def print_substep_error(msg: str) -> None:
    console.print(f"      [red]✗ Error:[/red] {msg}")

def print_header(template_lang: str, project_name: str, os_name: str) -> None:
    console.print(f"\n[bold]🚀 Creating {template_lang} project:[/bold] {project_name} ({os_name})\n")

def print_completed(project_name: str, template_lang: str, placeholders: dict) -> None:
    console.print(f"\n[green bold]✅ '{project_name}' ready![/green bold]\n")
    console.print("[bold]Next steps:[/bold]")
    console.print(f"  cd {project_name}")
    if template_lang == "python":
        console.print("  uv run src/main.py")
    else:
        req_cmd = placeholders.get("REQUIREMENTS_CMD", "./requirements.sh install")
        build_cmd = placeholders.get("BUILD_CMD", "./build.sh")
        console.print(f"  {req_cmd}    # (optional) install dependencies")
        console.print(f"  {build_cmd}                   # build & run")

def print_help(config: dict) -> None:
    console.print("[bold]tbuild[/bold] — Cross-platform project scaffolding tool\n")
    console.print("[bold]Usage:[/bold]")
    console.print("  tbuild init <language> <project_name>\n")
    console.print("[bold]Supported Languages (from templates.json):[/bold]")
    for name, info in config.items():
        aliases = f" ({', '.join(info['aliases'])})" if info.get("aliases") else ""
        desc = info.get("description", "")
        console.print(f"  {name:<12}{aliases:<10} {desc}")
    console.print("\n[bold]Examples:[/bold]")
    console.print("  tbuild init python my_py_app")
    console.print("  tbuild init cpp my_cpp_app")
    console.print("  tbuild init c my_c_lib")
