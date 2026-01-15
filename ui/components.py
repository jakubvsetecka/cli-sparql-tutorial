"""UI Components for the SPARQL tutorial."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.text import Text
from rich.style import Style
from rich import box

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.history import InMemoryHistory

# Try to import SPARQL lexer, fall back to SQL if not available
try:
    from pygments.lexers.rdf import SparqlLexer
except ImportError:
    from pygments.lexers.sql import SqlLexer as SparqlLexer

console = Console()

# Shared query history across sessions
query_history = InMemoryHistory()

# Custom style for the prompt
prompt_style = PTStyle.from_dict({
    'prompt': '#888888',
    'pygments.keyword': '#ff79c6 bold',
    'pygments.name.variable': '#50fa7b',
    'pygments.operator': '#ff79c6',
    'pygments.punctuation': '#f8f8f2',
    'pygments.literal.string': '#f1fa8c',
    'pygments.comment': '#6272a4 italic',
})


def clear_screen():
    """Clear the terminal screen."""
    console.clear()


def print_banner(text: str, style: str = "bold cyan"):
    """Print ASCII art banner with style."""
    console.print(text, style=style)


def print_concept(title: str, explanation: str):
    """Print a concept explanation in a styled panel."""
    panel = Panel(
        Markdown(explanation),
        title=f"[bold yellow]📚 {title}[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    )
    console.print(panel)


def print_example_query(query: str, description: str = None):
    """Print an example SPARQL query with syntax highlighting."""
    if description:
        console.print(f"\n[dim italic]{description}[/dim italic]")

    syntax = Syntax(query, "sparql", theme="monokai", line_numbers=True)
    panel = Panel(
        syntax,
        title="[bold green]Example Query[/bold green]",
        border_style="green",
        padding=(0, 1),
    )
    console.print(panel)


def print_exercise(number: int, task: str):
    """Print an exercise prompt."""
    panel = Panel(
        f"[bold white]{task}[/bold white]",
        title=f"[bold magenta]🚀 Exercise {number}[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(panel)


def print_hint(hint_text: str, hint_number: int = 1):
    """Print a hint in a styled panel."""
    icons = ["💡", "🔍", "🎯"]
    icon = icons[min(hint_number - 1, len(icons) - 1)]

    panel = Panel(
        f"[italic]{hint_text}[/italic]",
        title=f"[bold blue]{icon} Hint {hint_number}[/bold blue]",
        border_style="blue",
        padding=(0, 2),
    )
    console.print(panel)


def print_error(error_message: str):
    """Print an error message."""
    panel = Panel(
        f"[white]{error_message}[/white]",
        title="[bold red]❌ Error[/bold red]",
        border_style="red",
        padding=(0, 2),
    )
    console.print(panel)


def print_success(message: str = "Correct! Great job!"):
    """Print a success message."""
    panel = Panel(
        f"[bold white]{message}[/bold white]",
        title="[bold green]✓ Success[/bold green]",
        border_style="green",
        padding=(0, 2),
    )
    console.print(panel)


def print_results_table(results: list, variables: list):
    """Print query results in a formatted table."""
    if not results:
        console.print("[dim]No results found.[/dim]")
        return

    table = Table(
        title="[bold]Query Results[/bold]",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )

    for var in variables:
        table.add_column(str(var), style="white")

    for row in results[:50]:  # Limit to 50 rows for display
        table.add_row(*[str(row.get(var, "")) for var in variables])

    if len(results) > 50:
        console.print(f"[dim](Showing 50 of {len(results)} results)[/dim]")

    console.print(table)


def print_menu(title: str, options: list) -> str:
    """Print a menu and return the formatted options."""
    console.print(f"\n[bold cyan]═══ {title} ═══[/bold cyan]\n")

    for i, (key, label, status) in enumerate(options):
        if status == "completed":
            status_icon = "[green]✓[/green]"
        elif status == "current":
            status_icon = "[yellow]→[/yellow]"
        else:
            status_icon = "[dim]○[/dim]"

        console.print(f"  {status_icon} [{key}] {label}")

    console.print()


def print_progress(current: int, total: int, label: str = "Progress"):
    """Print a progress indicator."""
    percentage = int(100 * current / total) if total > 0 else 0
    filled = int(30 * current / total) if total > 0 else 0
    empty = 30 - filled

    bar = f"{'█' * filled}{'░' * empty}"
    console.print(f"\n[dim]{label}:[/dim] [{bar}] {current}/{total} ({percentage}%)")


def print_info(message: str):
    """Print an info message."""
    console.print(f"[cyan]ℹ[/cyan]  {message}")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[yellow]⚠[/yellow]  {message}")


def print_query_input_help():
    """Print help for the query input mode."""
    help_text = """
[dim]Editor Controls:[/dim]
  [cyan]Ctrl+Enter[/cyan] or [cyan]Esc Enter[/cyan]  - Execute query
  [cyan]↑ ↓ ← →[/cyan]                  - Move cursor
  [cyan]Tab[/cyan]                      - Insert spaces
  [cyan]Ctrl+↑/↓[/cyan]                 - Scroll through history

[dim]Commands (type and press Enter):[/dim]
  [cyan]hint[/cyan]      - Get a hint (up to 3 levels)
  [cyan]solution[/cyan]  - Show the solution
  [cyan]skip[/cyan]      - Skip this exercise
  [cyan]menu[/cyan]      - Return to main menu
  [cyan]quit[/cyan]      - Exit the tutorial
"""
    console.print(Panel(help_text, title="[bold]Help[/bold]", border_style="dim"))


def get_multiline_input(prompt: str = "Enter your SPARQL query") -> str:
    """Get multiline input using prompt_toolkit with full editing support."""
    console.print(f"\n[bold yellow]{prompt}[/bold yellow]")
    console.print("[dim](Ctrl+Enter or Esc,Enter to execute | Tab for indent | ↑↓ for history | Type 'help' for more)[/dim]\n")

    # Create key bindings
    bindings = KeyBindings()

    @bindings.add(Keys.ControlJ)  # Ctrl+Enter (some terminals)
    @bindings.add(Keys.Escape, Keys.Enter)  # Esc then Enter
    def submit(event):
        """Submit the query."""
        event.current_buffer.validate_and_handle()

    @bindings.add(Keys.Tab)
    def insert_tab(event):
        """Insert 4 spaces for tab."""
        event.current_buffer.insert_text("    ")

    # Create session with history and syntax highlighting
    session = PromptSession(
        multiline=True,
        lexer=PygmentsLexer(SparqlLexer),
        style=prompt_style,
        history=query_history,
        key_bindings=bindings,
        prompt_continuation=lambda width, line_number, is_soft_wrap: '     > ',
        enable_history_search=True,
    )

    try:
        text = session.prompt(
            [('class:prompt', 'SPARQL> ')],
            multiline=True,
        )

        # Check for special commands (single word commands)
        text_stripped = text.strip().lower()
        if text_stripped in ['help', 'hint', 'solution', 'skip', 'menu', 'quit', 'clear']:
            return f"__{text_stripped}__"

        return text

    except KeyboardInterrupt:
        return "__menu__"
    except EOFError:
        return "__quit__"


def confirm(message: str) -> bool:
    """Ask for confirmation."""
    response = console.input(f"[yellow]{message} (y/n): [/yellow]").strip().lower()
    return response in ['y', 'yes']


def wait_for_enter(message: str = "Press Enter to continue..."):
    """Wait for the user to press Enter."""
    console.input(f"\n[dim]{message}[/dim]")


def print_data_preview(data_description: str):
    """Print a preview of the available data."""
    panel = Panel(
        Markdown(data_description),
        title="[bold blue]🗃️ Available Data[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(panel)


def print_sparql_syntax(query: str):
    """Print a SPARQL query with syntax highlighting."""
    syntax = Syntax(query.strip(), "sparql", theme="monokai", line_numbers=False)
    console.print(syntax)


def print_divider(style: str = "dim"):
    """Print a divider line."""
    console.print(f"[{style}]{'─' * 80}[/{style}]")
