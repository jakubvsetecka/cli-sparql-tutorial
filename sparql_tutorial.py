#!/usr/bin/env python3
"""
SPARQL Tutorial - An Interactive CLI-based Tutorial for Beginners
Explore the Space Knowledge Graph and learn SPARQL!
"""

import sys
import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import box

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.ascii_art import (
    MAIN_BANNER, SUBTITLE, ROCKET, SATELLITE, ASTRONAUT,
    STARS_LINE, GOODBYE, TROPHY, get_progress_bar, get_lesson_header
)
from ui.components import (
    console, clear_screen, print_banner, print_concept, print_example_query,
    print_exercise, print_hint, print_error, print_success, print_results_table,
    print_progress, print_info, print_warning, print_query_input_help,
    get_multiline_input, wait_for_enter, print_divider, print_sparql_syntax,
    print_data_preview, confirm
)
from engine.sparql_engine import SPARQLEngine
from engine.shacl_engine import SHACLEngine
from engine.validator import QueryValidator, HintSystem
from lessons.content import LESSONS, DATA_DESCRIPTION


class SPARQLTutorial:
    """Main tutorial application."""

    def __init__(self):
        """Initialize the tutorial."""
        self.console = console
        self.engine = None
        self.shacl_engine = None
        self.validator = QueryValidator()
        self.hint_system = HintSystem()
        self.progress_file = Path(__file__).parent / ".progress.json"
        self.progress = self._load_progress()
        self.current_lesson = None

    def _load_progress(self) -> dict:
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file) as f:
                    return json.load(f)
            except:
                pass
        return {"completed_lessons": [], "current_lesson": 1}

    def _save_progress(self):
        """Save progress to file."""
        try:
            with open(self.progress_file, "w") as f:
                json.dump(self.progress, f)
        except:
            pass

    def _init_engine(self):
        """Initialize the SPARQL engine."""
        if self.engine is None:
            try:
                self.engine = SPARQLEngine()
                return True
            except FileNotFoundError as e:
                print_error(f"Could not load knowledge graph: {e}")
                return False
        return True

    def _init_shacl_engine(self):
        """Initialize the SHACL engine."""
        if self.shacl_engine is None:
            try:
                # Initialize SHACL engine with the same data as SPARQL engine
                if not self._init_engine():
                    return False
                self.shacl_engine = SHACLEngine(data_graph=self.engine.graph)
                return True
            except Exception as e:
                print_error(f"Could not initialize SHACL engine: {e}")
                return False
        return True

    def show_welcome(self):
        """Show the welcome screen."""
        clear_screen()
        print_banner(MAIN_BANNER, "bold cyan")
        print_banner(SUBTITLE, "bold white")
        console.print(STARS_LINE, style="yellow")
        console.print()

        # Show stats if engine is loaded
        if self._init_engine():
            stats = self.engine.get_stats()
            stats_text = (
                f"[cyan]Knowledge Graph Loaded![/cyan]\n"
                f"  {stats['total_triples']} triples | "
                f"{stats['planets']} planets | "
                f"{stats['astronauts']} astronauts | "
                f"{stats['missions']} missions"
            )
            console.print(Panel(stats_text, border_style="green"))

        wait_for_enter()

    def show_main_menu(self):
        """Show the main menu and handle navigation."""
        while True:
            clear_screen()
            print_banner(SATELLITE, "cyan")
            console.print("\n[bold cyan]═══ SPARQL TUTORIAL - MAIN MENU ═══[/bold cyan]\n")

            # Show progress
            completed = len(self.progress["completed_lessons"])
            total = len(LESSONS)
            console.print(get_progress_bar(completed, total))
            console.print()

            # Build menu options
            console.print("[bold]Lessons:[/bold]\n")

            for i, lesson in enumerate(LESSONS):
                lesson_id = lesson["id"]
                status = "✓" if lesson_id in self.progress["completed_lessons"] else "○"
                color = "green" if lesson_id in self.progress["completed_lessons"] else "white"
                current_marker = " [yellow]← current[/yellow]" if lesson_id == self.progress["current_lesson"] else ""

                console.print(
                    f"  [{color}]{status}[/{color}] [{lesson_id:2d}] {lesson['title']} "
                    f"[dim]({lesson['category']})[/dim]{current_marker}"
                )

            console.print("\n[bold]Options:[/bold]\n")
            console.print("  [D] View available data")
            console.print("  [F] Free query mode (sandbox)")
            console.print("  [S] SHACL constraints mode")
            console.print("  [R] Reset progress")
            console.print("  [Q] Quit")

            console.print()
            choice = console.input("[bold yellow]Enter choice: [/bold yellow]").strip()

            if choice.lower() == 'q':
                self.show_goodbye()
                return

            if choice.lower() == 'd':
                self.show_data_explorer()
                continue

            if choice.lower() == 'f':
                self.free_query_mode()
                continue

            if choice.lower() == 's':
                self.shacl_free_mode()
                continue

            if choice.lower() == 'r':
                if confirm("Reset all progress?"):
                    self.progress = {"completed_lessons": [], "current_lesson": 1}
                    self._save_progress()
                    print_success("Progress reset!")
                    wait_for_enter()
                continue

            # Try to parse as lesson number
            try:
                lesson_num = int(choice)
                if 1 <= lesson_num <= len(LESSONS):
                    self.run_lesson(lesson_num)
            except ValueError:
                print_warning("Invalid choice. Enter a lesson number or menu option.")
                wait_for_enter()

    def show_data_explorer(self):
        """Show available data in the knowledge graph."""
        clear_screen()
        print_banner(ROCKET, "yellow")
        console.print("\n[bold cyan]═══ DATA EXPLORER ═══[/bold cyan]\n")

        print_data_preview(DATA_DESCRIPTION)

        console.print("\n[bold]Quick Queries to Try:[/bold]\n")

        examples = [
            ("List all planets", "SELECT ?name WHERE { ?p a :Planet . ?p :name ?name }"),
            ("List all astronauts", "SELECT ?name WHERE { ?a a :Astronaut . ?a :name ?name }"),
            ("Show missions", "SELECT ?name ?date WHERE { ?m a :Mission . ?m :name ?name . OPTIONAL { ?m :launchDate ?date } }"),
        ]

        for desc, query in examples:
            console.print(f"[cyan]{desc}:[/cyan]")
            console.print(f"[dim]{query}[/dim]\n")

        wait_for_enter()

    def free_query_mode(self):
        """Free-form query sandbox."""
        clear_screen()
        console.print("\n[bold cyan]═══ FREE QUERY MODE ═══[/bold cyan]\n")
        console.print("[dim]Execute any SPARQL query against the space knowledge graph.[/dim]")
        console.print("[dim]Type 'menu' to return to main menu, 'help' for query help.[/dim]\n")

        if not self._init_engine():
            wait_for_enter()
            return

        while True:
            query = get_multiline_input("Enter your SPARQL query")

            if query == "__menu__":
                return
            if query == "__quit__":
                self.show_goodbye()
                sys.exit(0)
            if query == "__help__":
                print_query_input_help()
                print_data_preview(DATA_DESCRIPTION)
                continue
            if query == "__clear__":
                clear_screen()
                console.print("\n[bold cyan]═══ FREE QUERY MODE ═══[/bold cyan]\n")
                continue

            if not query.strip():
                continue

            # Execute the query
            result = self.engine.execute(query)

            if result["success"]:
                console.print()
                if result["result_type"] == "SELECT":
                    print_results_table(result["results"], result["variables"])
                    console.print(f"\n[dim]{result['count']} results returned[/dim]")
                elif result["result_type"] == "ASK":
                    answer = result["ask_result"]
                    color = "green" if answer else "red"
                    console.print(f"\n[bold {color}]Result: {answer}[/bold {color}]")
                elif result["result_type"] == "CONSTRUCT":
                    console.print("\n[bold]Constructed Triples:[/bold]")
                    print_results_table(result["results"], result["variables"])
                else:
                    console.print(f"\n[dim]Query type: {result['result_type']}[/dim]")
            else:
                print_error(result["error"])

            console.print()

    def shacl_free_mode(self):
        """SHACL constraints sandbox for creating and validating shapes."""
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
        console.print("[dim]Create and validate SHACL constraints against the space knowledge graph.[/dim]")
        console.print("[dim]Type 'menu' to return to main menu, 'help' for commands.[/dim]\n")

        if not self._init_shacl_engine():
            wait_for_enter()
            return

        # Show initial stats
        stats = self.shacl_engine.get_stats()
        console.print(f"[cyan]Data loaded:[/cyan] {stats['total_data_triples']} triples\n")

        while True:
            console.print("[bold]SHACL Commands:[/bold]")
            console.print("  [green]add[/green]      - Add a SHACL shape constraint")
            console.print("  [green]validate[/green] - Validate data against loaded shapes")
            console.print("  [green]examples[/green] - Load example SHACL shapes")
            console.print("  [green]clear[/green]    - Clear all loaded shapes")
            console.print("  [green]stats[/green]    - Show current shapes statistics")
            console.print("  [green]help[/green]     - Show SHACL commands and guidance")
            console.print("  [green]quit[/green]     - Exit the tutorial")
            console.print("  [green]menu[/green]     - Return to main menu")
            console.print()

            command = console.input("[bold yellow]Enter command: [/bold yellow]").strip().lower()

            if command == "menu":
                return
            
            if command == "quit":
                self.show_goodbye()
                sys.exit(0)

            if command == "help":
                self._show_shacl_help()
                continue

            if command == "stats":
                stats = self.shacl_engine.get_stats()
                console.print(f"\n[cyan]Current Statistics:[/cyan]")
                console.print(f"  Loaded shapes: {stats['total_shapes']}")
                console.print(f"  Shape triples: {stats['total_shape_triples']}")
                console.print(f"  Data triples: {stats['total_data_triples']}")
                console.print()
                wait_for_enter()
                clear_screen()
                console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
                continue

            if command == "clear":
                self.shacl_engine.clear_shapes()
                print_success("All SHACL shapes cleared!")
                wait_for_enter()
                clear_screen()
                console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
                continue

            if command == "examples":
                self._load_example_shapes()
                continue

            if command == "add":
                self._add_shacl_shape()
                continue

            if command == "validate":
                self._validate_with_shacl()
                continue

            print_warning("Unknown command. Type 'help' for available commands.")
            console.print()

    def _show_shacl_help(self):
        """Show help information for SHACL mode."""
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL HELP ═══[/bold cyan]\n")
        
        console.print("[bold]What is SHACL?[/bold]")
        console.print("SHACL (Shapes Constraint Language) validates RDF graphs against constraints.")
        console.print("You can define 'shapes' that describe what valid data should look like.\n")
        
        console.print("[bold]Example SHACL Shape:[/bold]\n")
        example = """@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:PlanetShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :diameter ;
        sh:minInclusive 1000 ;
        sh:message "Planet diameter must be >= 1000 km" ;
    ] ."""
        
        from ui.components import print_sparql_syntax
        print_sparql_syntax(example)
        
        console.print("\n[bold]Common Constraints:[/bold]")
        console.print("  • sh:minCount, sh:maxCount - Cardinality")
        console.print("  • sh:datatype - Data type validation")
        console.print("  • sh:minInclusive, sh:maxInclusive - Value ranges")
        console.print("  • sh:pattern - Regex patterns")
        console.print("  • sh:nodeKind - IRI, Literal, or BlankNode")
        console.print()
        
        wait_for_enter()
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")

    def _load_example_shapes(self):
        """Load example SHACL shapes."""
        clear_screen()
        console.print("\n[bold cyan]═══ EXAMPLE SHACL SHAPES ═══[/bold cyan]\n")
        
        examples = self.shacl_engine.get_example_shapes()
        
        console.print("[bold]Available Examples:[/bold]\n")
        for i, (name, shape) in enumerate(examples.items(), 1):
            console.print(f"  [{i}] {name.replace('_', ' ').title()}")
        
        console.print("  [A] Load all examples")
        console.print("  [C] Cancel\n")
        
        choice = console.input("[bold yellow]Select example(s): [/bold yellow]").strip().lower()
        
        if choice == 'c':
            clear_screen()
            console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
            return
        
        if choice == 'a':
            # Load all examples
            for name, shape in examples.items():
                success, error = self.shacl_engine.add_shape_from_text(shape)
                if not success:
                    print_error(f"Error loading {name}: {error}")
            print_success(f"Loaded all {len(examples)} example shapes!")
        else:
            try:
                idx = int(choice) - 1
                name = list(examples.keys())[idx]
                shape = examples[name]
                
                console.print(f"\n[bold]Loading: {name.replace('_', ' ').title()}[/bold]\n")
                from ui.components import print_sparql_syntax
                print_sparql_syntax(shape)
                console.print()
                
                success, error = self.shacl_engine.add_shape_from_text(shape)
                if success:
                    print_success(f"Shape '{name}' loaded successfully!")
                else:
                    print_error(f"Error: {error}")
            except (ValueError, IndexError):
                print_warning("Invalid selection")
        
        wait_for_enter()
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")

    def _add_shacl_shape(self):
        """Add a custom SHACL shape."""
        clear_screen()
        console.print("\n[bold cyan]═══ ADD SHACL SHAPE ═══[/bold cyan]\n")
        console.print("[dim]Enter your SHACL shape in Turtle format.[/dim]")
        console.print("[dim]Type your shape, then press Ctrl+Enter or Esc,Enter to submit.[/dim]\n")
        
        shape = get_multiline_input("Enter SHACL shape")
        
        # Handle special control tokens from get_multiline_input
        if shape == "__menu__":
            clear_screen()
            console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
            return
        if shape == "__quit__":
            clear_screen()
            console.print(GOODBYE)
            sys.exit(0)
        if shape == "__help__":
            print_query_input_help()
            wait_for_enter()
            # Re-enter SHACL shape input after showing help
            self._add_shacl_shape()
            return
        if shape == "__clear__":
            clear_screen()
            # Re-enter SHACL shape input after clearing the screen
            self._add_shacl_shape()
            return

        if shape == "__help__":
            self._show_shacl_help()
            return self._add_shacl_shape()

        if not shape.strip():
            print_warning("No shape entered")
            wait_for_enter()
            clear_screen()
            console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
            return
        
        success, error = self.shacl_engine.add_shape_from_text(shape)
        
        if success:
            print_success("SHACL shape added successfully!")
            stats = self.shacl_engine.get_stats()
            console.print(f"\n[dim]Total shapes loaded: {stats['total_shapes']}[/dim]")
        else:
            print_error(f"Failed to add shape:\n{error}")
        
        wait_for_enter()
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")

    def _validate_with_shacl(self):
        """Validate the data graph against loaded SHACL shapes."""
        stats = self.shacl_engine.get_stats()
        
        if stats['total_shapes'] == 0:
            print_warning("No SHACL shapes loaded! Use 'add' or 'examples' to load shapes first.")
            wait_for_enter()
            clear_screen()
            console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
            return
        
        clear_screen()
        console.print("\n[bold cyan]═══ VALIDATING DATA ═══[/bold cyan]\n")
        console.print(f"[dim]Validating {stats['total_data_triples']} triples against {stats['total_shapes']} shape(s)...[/dim]\n")
        
        # Perform validation
        result = self.shacl_engine.validate()
        
        if not result["success"]:
            print_error(f"Validation failed: {result['error']}")
            wait_for_enter()
            clear_screen()
            console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")
            return
        
        # Display results
        if result["conforms"]:
            console.print("[bold green]✓ VALIDATION PASSED[/bold green]")
            console.print("\n[green]All data conforms to the SHACL constraints![/green]\n")
        else:
            console.print("[bold red]✗ VALIDATION FAILED[/bold red]")
            console.print(f"\n[red]Found {result['violation_count']} violation(s):[/red]\n")
            
            # Display violations in a table
            if result["violations"]:
                from rich.table import Table
                
                table = Table(title="SHACL Violations", box=box.ROUNDED)
                table.add_column("Focus Node", style="cyan")
                table.add_column("Property", style="yellow")
                table.add_column("Value", style="white")
                table.add_column("Message", style="red")
                table.add_column("Severity", style="magenta")
                
                for v in result["violations"][:20]:  # Show max 20
                    table.add_row(
                        v["focus_node"] or "",
                        v["property"] or "",
                        v["value"] or "",
                        v["message"],
                        v["severity"]
                    )
                
                console.print(table)
                
                if len(result["violations"]) > 20:
                    console.print(f"\n[dim]... and {len(result['violations']) - 20} more violations[/dim]")
                
                # Show fix suggestions
                console.print("\n[bold]Fix Suggestions:[/bold]")
                for i, v in enumerate(result["violations"][:5], 1):
                    if v["fix_suggestion"]:
                        console.print(f"  {i}. {v['fix_suggestion']}")
                
                console.print()
        
        wait_for_enter()
        clear_screen()
        console.print("\n[bold cyan]═══ SHACL CONSTRAINTS MODE ═══[/bold cyan]\n")

    def run_lesson(self, lesson_num: int):
        """Run a specific lesson."""
        if not self._init_engine():
            wait_for_enter()
            return

        lesson = LESSONS[lesson_num - 1]
        self.current_lesson = lesson
        self.progress["current_lesson"] = lesson_num
        self._save_progress()

        # Show lesson intro
        clear_screen()
        console.print(get_lesson_header(lesson["id"], lesson["title"]))
        console.print(STARS_LINE, style="dim yellow")
        console.print()

        # Show concept explanation
        print_concept(lesson["title"], lesson["concept"])
        wait_for_enter("Press Enter to start the exercises...")

        # Run exercises
        for i, exercise in enumerate(lesson["exercises"]):
            if not self.run_exercise(lesson, exercise, i + 1):
                # User chose to go back to menu
                return

        # Lesson complete!
        self.mark_lesson_complete(lesson_num)

    def run_exercise(self, lesson: dict, exercise: dict, exercise_num: int) -> bool:
        """
        Run a single exercise.

        Returns:
            True to continue to next exercise, False to return to menu
        """
        exercise_id = f"{lesson['id']}_{exercise_num}"
        self.hint_system.reset_hints(exercise_id)
        hints_used = 0
        max_hints = len(exercise.get("hints", []))

        while True:
            clear_screen()
            console.print(get_lesson_header(lesson["id"], lesson["title"]))
            print_exercise(exercise_num, exercise["task"])
            console.print()

            # Show hint status
            if hints_used > 0:
                console.print(f"[dim]Hints used: {hints_used}/{max_hints}[/dim]")

            print_query_input_help()

            query = get_multiline_input()

            # Handle special commands
            if query == "__menu__":
                return False

            if query == "__quit__":
                self.show_goodbye()
                sys.exit(0)

            if query == "__hint__":
                hints_used = self.hint_system.increment_hint(exercise_id)
                hint_text = self.validator.get_progressive_hint(exercise, hints_used)
                if hint_text:
                    print_hint(hint_text, hints_used)
                else:
                    print_warning("No more hints available!")
                wait_for_enter()
                continue

            if query == "__solution__":
                console.print("\n[bold yellow]Solution:[/bold yellow]\n")
                print_sparql_syntax(exercise["solution"])
                wait_for_enter("\nStudy the solution, then press Enter to try again...")
                continue

            if query == "__skip__":
                if confirm("Skip this exercise?"):
                    print_warning("Skipping exercise...")
                    wait_for_enter()
                    return True
                continue

            if query == "__clear__":
                continue

            if query == "__help__":
                print_query_input_help()
                wait_for_enter()
                continue

            if not query.strip():
                continue

            # Execute the query
            result = self.engine.execute(query)

            if not result["success"]:
                print_error(result["error"])

                # Offer specific help based on error
                analysis = self.validator.analyze_error(result.get("raw_error", result["error"]))
                if analysis:
                    console.print(f"\n[dim]{analysis}[/dim]")

                wait_for_enter()
                continue

            # Show results
            console.print()
            if result["result_type"] == "SELECT":
                print_results_table(result["results"], result["variables"])
            elif result["result_type"] == "ASK":
                answer = result["ask_result"]
                color = "green" if answer else "red"
                console.print(f"\n[bold {color}]ASK Result: {answer}[/bold {color}]")
            elif result["result_type"] == "CONSTRUCT":
                console.print("\n[bold]Constructed Triples:[/bold]")
                print_results_table(result["results"][:20], result["variables"])
                if len(result["results"]) > 20:
                    console.print(f"[dim]... and {len(result['results']) - 20} more[/dim]")

            # Validate against expected results
            try:
                is_correct = exercise["validate"](result["results"])
            except Exception:
                is_correct = result["success"]  # Fallback

            if is_correct:
                console.print()
                print_success(exercise.get("success_message", "Correct! Great job!"))
                wait_for_enter("\nPress Enter to continue...")
                return True
            else:
                print_warning(
                    "Your query ran successfully, but the results don't match what we're looking for.\n"
                    "Try again or use 'hint' for help!"
                )
                wait_for_enter()

    def mark_lesson_complete(self, lesson_num: int):
        """Mark a lesson as complete and show celebration."""
        if lesson_num not in self.progress["completed_lessons"]:
            self.progress["completed_lessons"].append(lesson_num)

        # Update current lesson to next
        if lesson_num < len(LESSONS):
            self.progress["current_lesson"] = lesson_num + 1
        self._save_progress()

        # Show completion screen
        clear_screen()

        if lesson_num == len(LESSONS):
            # Final lesson complete!
            console.print(TROPHY, style="bold yellow")
            console.print("\n[bold green]🎉 CONGRATULATIONS! 🎉[/bold green]")
            console.print("\n[bold]You have completed the entire SPARQL tutorial![/bold]")
            console.print("\nYou are now a SPARQL expert, ready to query any knowledge graph!")
        else:
            console.print("\n[bold green]✓ LESSON COMPLETE![/bold green]")
            console.print(f"\nYou've completed lesson {lesson_num}: {LESSONS[lesson_num-1]['title']}")

        # Show progress
        completed = len(self.progress["completed_lessons"])
        total = len(LESSONS)
        console.print(f"\n{get_progress_bar(completed, total)}")

        wait_for_enter()

    def show_goodbye(self):
        """Show goodbye screen."""
        clear_screen()
        console.print(GOODBYE, style="cyan")


def main():
    """Main entry point."""
    tutorial = SPARQLTutorial()

    try:
        tutorial.show_welcome()
        tutorial.show_main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[dim]Tutorial interrupted. Goodbye![/dim]")
        sys.exit(0)


if __name__ == "__main__":
    main()
