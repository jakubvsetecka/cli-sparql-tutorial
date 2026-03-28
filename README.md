# SPARQL Tutorial CLI

An interactive command-line tutorial for learning SPARQL, the query language for RDF graph databases.

```
  ██████  ██▓███   ▄▄▄       ██▀███    ▄████   ██▓
▒██    ▒ ▓██░  ██▒▒████▄    ▓██ ▒ ██▒ ██▒ ▀█▒ ▓██▒
░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄  ▓██ ░▄█ ▒▒██░▄▄▄░ ▒██░
  ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██▀▀█▄  ░▓█  ██▓ ▒██░
▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒░██▓ ▒██▒░▒▓███▀▒ ░██████▒
```

## Features

- **16 Progressive Lessons** - From basic SELECT queries to advanced subqueries and property paths
- **Interactive Exercises** - Practice each concept with hands-on exercises
- **Built-in Knowledge Graph** - Explore a space exploration dataset with planets, astronauts, missions, and more
- **SHACL Constraints Mode** - Create and validate SHACL shapes for data quality assurance (NEW!)
- **Syntax Highlighting** - Full SPARQL syntax highlighting in the editor
- **Smart Hints** - 3-level progressive hint system when you get stuck
- **Friendly Error Messages** - Clear explanations of syntax errors
- **Progress Tracking** - Your progress is saved between sessions
- **Rich Text Editor** - Full cursor navigation, tab indentation, and query history

## Installation

```bash
git clone https://github.com/yourusername/cli-sparql-tutorial.git
cd cli-sparql-tutorial
./run.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sparql_tutorial.py
```

## What You'll Learn

### Beginner
1. Introduction to SPARQL and RDF
2. Basic SELECT Queries
3. Triple Patterns (Subject-Predicate-Object)
4. Multiple Patterns and Joins
5. FILTER - Constraining Results
6. OPTIONAL - Handling Missing Data
7. ORDER BY and LIMIT

### Intermediate
8. DISTINCT - Removing Duplicates
9. COUNT and GROUP BY - Aggregations
10. UNION - Combining Patterns
11. BIND and Expressions - Computed Values

### Advanced
12. Subqueries - Nested Queries
13. Property Paths - Following Relationships
14. CONSTRUCT - Building New Graphs
15. ASK and DESCRIBE Queries
16. Final Challenge

## The Dataset

The tutorial uses a space exploration knowledge graph containing:

| Entity | Count | Properties |
|--------|-------|------------|
| Planets | 8 | name, diameter, distance from sun, moons, rings |
| Moons | 10 | name, diameter, orbits |
| Astronauts | 12 | name, nationality, birth year, moonwalker status |
| Missions | 13 | name, launch date, destination, crew, success |
| Space Agencies | 6 | name, founded, headquarters |
| Spacecraft | 7 | name |

## SHACL Constraints Mode

In addition to learning SPARQL queries, you can now explore SHACL (Shapes Constraint Language) for validating RDF data!

### What You Can Do

- **Create Custom Shapes** - Define data quality constraints in Turtle format
- **Load Examples** - Five pre-built example shapes to get started
- **Validate Data** - Run validation against the knowledge graph
- **View Violations** - See detailed violation reports with fix suggestions
- **Manage Shapes** - Add, clear, and inspect loaded shapes

### Quick Start

1. Run the tutorial: `python3 sparql_tutorial.py`
2. Select `[S] SHACL constraints mode` from the main menu
3. Try `examples` to load pre-built shapes
4. Use `validate` to check data quality
5. Create your own shapes with `add`

### Example Use Cases

- Ensure all planets have valid diameter values
- Validate astronaut name requirements
- Check mission date formats
- Enforce data type constraints
- Verify relationship integrity

For detailed documentation, see [SHACL_GUIDE.md](SHACL_GUIDE.md).

To see demos of the SHACL functionality, run:
```bash
python3 demo_shacl.py
```

## Editor Controls

| Key | Action |
|-----|--------|
| `↑ ↓ ← →` | Move cursor |
| `Tab` | Insert indentation |
| `Enter` | New line |
| `Ctrl+Enter` or `Esc, Enter` | Execute query |
| `Ctrl+↑/↓` | Browse query history |

## Commands

| Command | Description |
|---------|-------------|
| `hint` | Get a progressive hint |
| `solution` | Show the solution |
| `skip` | Skip current exercise |
| `menu` | Return to main menu |
| `quit` | Exit tutorial |

## Requirements

- Python 3.8+
- Terminal with Unicode support

## Dependencies

- `rdflib` - RDF graph library and SPARQL engine
- `pyshacl` - SHACL validation engine
- `rich` - Beautiful terminal formatting
- `prompt_toolkit` - Advanced input handling
- `pygments` - Syntax highlighting

## License

MIT
