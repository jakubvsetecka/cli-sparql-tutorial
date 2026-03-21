#!/usr/bin/env python3
"""
SHACL Feature Demo Script
Demonstrates the SHACL validation capabilities
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.shacl_engine import SHACLEngine
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def demo_basic_validation():
    """Demo: Basic SHACL validation"""
    console.print("\n[bold cyan]═══ DEMO 1: Basic Validation ═══[/bold cyan]\n")
    
    # Initialize engine
    engine = SHACLEngine()
    
    # Add a simple shape
    shape = """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:PlanetDiameterShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :diameter ;
        sh:minInclusive 1000 ;
        sh:message "Planet diameter must be at least 1000 km" ;
    ] .
"""
    
    console.print("[yellow]Adding SHACL shape:[/yellow]")
    console.print(shape)
    
    success, error = engine.add_shape_from_text(shape)
    
    if success:
        console.print("[green]✓ Shape added successfully[/green]\n")
    else:
        console.print(f"[red]✗ Error: {error}[/red]\n")
        return
    
    # Validate
    console.print("[yellow]Validating data...[/yellow]\n")
    result = engine.validate()
    
    if result["conforms"]:
        console.print("[bold green]✓ VALIDATION PASSED[/bold green]")
        console.print("All planets have valid diameters!\n")
    else:
        console.print(f"[bold red]✗ VALIDATION FAILED[/bold red]")
        console.print(f"Found {result['violation_count']} violation(s)\n")


def demo_multiple_constraints():
    """Demo: Multiple constraints"""
    console.print("\n[bold cyan]═══ DEMO 2: Multiple Constraints ═══[/bold cyan]\n")
    
    engine = SHACLEngine()
    
    # Load all example shapes
    examples = engine.get_example_shapes()
    
    console.print(f"[yellow]Loading {len(examples)} example shapes...[/yellow]\n")
    
    for name, shape in examples.items():
        success, error = engine.add_shape_from_text(shape)
        if success:
            console.print(f"  [green]✓[/green] {name}")
        else:
            console.print(f"  [red]✗[/red] {name}: {error}")
    
    console.print()
    
    # Show stats
    stats = engine.get_stats()
    console.print(f"[cyan]Statistics:[/cyan]")
    console.print(f"  Loaded shapes: {stats['total_shapes']}")
    console.print(f"  Shape triples: {stats['total_shape_triples']}")
    console.print(f"  Data triples: {stats['total_data_triples']}")
    console.print()
    
    # Validate
    console.print("[yellow]Validating data against all shapes...[/yellow]\n")
    result = engine.validate()
    
    if result["conforms"]:
        console.print("[bold green]✓ ALL VALIDATIONS PASSED[/bold green]")
        console.print("Data conforms to all constraints!\n")
    else:
        console.print(f"[bold yellow]⚠ Found {result['violation_count']} violation(s)[/bold yellow]\n")
        
        # Show sample violations
        if result["violations"]:
            table = Table(title="Sample Violations", box=box.ROUNDED)
            table.add_column("Focus Node", style="cyan")
            table.add_column("Property", style="yellow")
            table.add_column("Message", style="white")
            
            for v in result["violations"][:5]:
                table.add_row(
                    v["focus_node"] or "",
                    v["property"] or "",
                    v["message"]
                )
            
            console.print(table)
            console.print()


def demo_custom_shape():
    """Demo: Creating custom shapes"""
    console.print("\n[bold cyan]═══ DEMO 3: Custom Shape Creation ═══[/bold cyan]\n")
    
    engine = SHACLEngine()
    
    # Create a custom shape for astronaut validation
    custom_shape = """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:AstronautBirthYearShape a sh:NodeShape ;
    sh:targetClass :Astronaut ;
    sh:property [
        sh:path :birthYear ;
        sh:minInclusive 1900 ;
        sh:maxInclusive 2100 ;
        sh:datatype xsd:integer ;
        sh:message "Astronaut birth year must be between 1900 and 2100" ;
    ] .
"""
    
    console.print("[yellow]Custom Shape: Astronaut Birth Year Validation[/yellow]")
    console.print(custom_shape)
    
    success, error = engine.add_shape_from_text(custom_shape)
    
    if success:
        console.print("[green]✓ Custom shape added successfully[/green]\n")
        
        # Validate
        result = engine.validate()
        
        if result["conforms"]:
            console.print("[bold green]✓ VALIDATION PASSED[/bold green]")
            console.print("All astronauts have valid birth years!\n")
        else:
            console.print(f"[bold red]✗ VALIDATION FAILED[/bold red]")
            console.print(f"Found {result['violation_count']} violation(s)\n")
            
            for v in result["violations"]:
                console.print(f"  • {v['focus_node']}: {v['message']}")
            console.print()
    else:
        console.print(f"[red]✗ Error: {error}[/red]\n")


def demo_shape_management():
    """Demo: Managing shapes"""
    console.print("\n[bold cyan]═══ DEMO 4: Shape Management ═══[/bold cyan]\n")
    
    engine = SHACLEngine()
    
    # Add some shapes
    console.print("[yellow]Adding shapes...[/yellow]\n")
    
    shape1 = engine.get_example_shapes()["planet_diameter_constraint"]
    shape2 = engine.get_example_shapes()["astronaut_name_required"]
    
    engine.add_shape_from_text(shape1)
    engine.add_shape_from_text(shape2)
    
    stats = engine.get_stats()
    console.print(f"  Shapes loaded: {stats['total_shapes']}")
    console.print()
    
    # Clear shapes
    console.print("[yellow]Clearing all shapes...[/yellow]\n")
    engine.clear_shapes()
    
    stats = engine.get_stats()
    console.print(f"  Shapes loaded: {stats['total_shapes']}")
    console.print()
    
    # Add again
    console.print("[yellow]Re-adding shapes...[/yellow]\n")
    engine.add_shape_from_text(shape1)
    
    stats = engine.get_stats()
    console.print(f"  Shapes loaded: {stats['total_shapes']}")
    console.print()


def demo_violation_details():
    """Demo: Detailed violation information"""
    console.print("\n[bold cyan]═══ DEMO 5: Violation Details ═══[/bold cyan]\n")
    
    engine = SHACLEngine()
    
    # Add a shape that will likely have violations if we modify data
    shape = """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:StrictPlanetShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Planet must have exactly one name" ;
    ] ;
    sh:property [
        sh:path :diameter ;
        sh:minCount 1 ;
        sh:datatype xsd:integer ;
        sh:message "Planet must have an integer diameter" ;
    ] ;
    sh:property [
        sh:path :distanceFromSun ;
        sh:minCount 1 ;
        sh:datatype xsd:decimal ;
        sh:message "Planet must have a distance from sun" ;
    ] .
"""
    
    console.print("[yellow]Adding comprehensive planet validation shape...[/yellow]\n")
    engine.add_shape_from_text(shape)
    
    result = engine.validate()
    
    if result["conforms"]:
        console.print("[bold green]✓ ALL PLANETS VALID[/bold green]\n")
    else:
        console.print(f"[bold yellow]Found {result['violation_count']} violation(s)[/bold yellow]\n")
        
        # Show detailed violation information
        for i, v in enumerate(result["violations"][:3], 1):
            console.print(f"[bold]Violation {i}:[/bold]")
            console.print(f"  Focus Node: {v['focus_node']}")
            console.print(f"  Property: {v['property']}")
            console.print(f"  Value: {v['value']}")
            console.print(f"  Message: {v['message']}")
            console.print(f"  Severity: {v['severity']}")
            console.print(f"  Fix: {v['fix_suggestion']}")
            console.print()


def main():
    """Run all demos"""
    console.print("\n[bold magenta]╔═══════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║   SHACL VALIDATION DEMO SUITE         ║[/bold magenta]")
    console.print("[bold magenta]╚═══════════════════════════════════════╝[/bold magenta]")
    
    try:
        demo_basic_validation()
        input("\nPress Enter to continue to next demo...")
        
        demo_multiple_constraints()
        input("\nPress Enter to continue to next demo...")
        
        demo_custom_shape()
        input("\nPress Enter to continue to next demo...")
        
        demo_shape_management()
        input("\nPress Enter to continue to next demo...")
        
        demo_violation_details()
        
        console.print("\n[bold green]═══ ALL DEMOS COMPLETED ═══[/bold green]\n")
        console.print("[cyan]To explore interactively, run:[/cyan]")
        console.print("  python sparql_tutorial.py")
        console.print("\n[cyan]Then select option [S] for SHACL mode![/cyan]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[dim]Demo interrupted.[/dim]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
