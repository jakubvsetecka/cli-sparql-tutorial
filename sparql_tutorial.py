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
from engine.validator import QueryValidator, HintSystem
from lessons.content import LESSONS, DATA_DESCRIPTION


class SPARQLTutorial:
    """Main tutorial application."""

    def __init__(self):
        """Initialize the tutorial."""
        self.console = console
        self.engine = None
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
