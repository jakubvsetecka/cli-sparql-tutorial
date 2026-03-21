# SHACL Constraints Mode - Documentation

## Overview

The SHACL (Shapes Constraint Language) mode extends the SPARQL tutorial with data validation capabilities. You can now create, load, and validate SHACL constraints against the space exploration knowledge graph.

## What is SHACL?

SHACL is a W3C standard for validating RDF graphs. It allows you to define "shapes" that describe the expected structure and constraints of your data. When you validate your data against these shapes, SHACL reports any violations.

## Features

### 1. Interactive SHACL Environment
- Create custom SHACL shapes in Turtle format
- Load pre-built example shapes
- Validate data against loaded constraints
- View detailed violation reports with fix suggestions
- Clear and manage loaded shapes

### 2. Example Shapes Included

The system comes with five example SHACL shapes:

#### Planet Diameter Constraint
Ensures planet diameters are realistic (between 1,000 and 1,000,000 km).

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:PlanetShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :diameter ;
        sh:minInclusive 1000 ;
        sh:maxInclusive 1000000 ;
        sh:datatype xsd:integer ;
        sh:message "Planet diameter must be between 1,000 and 1,000,000 km" ;
    ] .
```

#### Astronaut Name Required
Validates that every astronaut has exactly one name.

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

:AstronautShape a sh:NodeShape ;
    sh:targetClass :Astronaut ;
    sh:property [
        sh:path :name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:message "Every astronaut must have exactly one name" ;
    ] .
```

#### Mission Date Format
Ensures mission launch dates are in proper date format.

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

:MissionShape a sh:NodeShape ;
    sh:targetClass :Mission ;
    sh:property [
        sh:path :launchDate ;
        sh:datatype xsd:date ;
        sh:message "Mission launch date must be in date format (YYYY-MM-DD)" ;
    ] .
```

#### Planet Moons Constraint
Validates that the number of moons is non-negative.

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:PlanetMoonsShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :numberOfMoons ;
        sh:minInclusive 0 ;
        sh:datatype xsd:integer ;
        sh:message "Number of moons cannot be negative" ;
    ] .
```

#### Complex Mission Validation
A multi-constraint shape validating mission data quality.

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

:ComplexMissionShape a sh:NodeShape ;
    sh:targetClass :Mission ;
    sh:property [
        sh:path :name ;
        sh:minCount 1 ;
        sh:message "Mission must have a name" ;
    ] ;
    sh:property [
        sh:path :destination ;
        sh:nodeKind sh:IRI ;
        sh:message "Mission destination must be a valid IRI" ;
    ] ;
    sh:property [
        sh:path :successful ;
        sh:datatype xsd:boolean ;
        sh:message "Mission success status must be boolean" ;
    ] .
```

## Usage Guide

### Accessing SHACL Mode

1. Start the tutorial: `python sparql_tutorial.py`
2. From the main menu, select `[S] SHACL constraints mode`

### Available Commands

In SHACL mode, you can use these commands:

- **add** - Create and add a custom SHACL shape
- **validate** - Validate the data graph against loaded shapes
- **examples** - Load pre-built example shapes
- **clear** - Remove all loaded shapes
- **stats** - View statistics about loaded shapes
- **menu** - Return to main menu

### Workflow Example

1. **Load Example Shapes**
   ```
   Command: examples
   Select: A (load all)
   ```

2. **Validate Data**
   ```
   Command: validate
   ```
   
3. **Review Violations**
   - The system displays violations in a table
   - Each violation shows:
     - Focus Node: The entity with the issue
     - Property: The problematic property
     - Value: The invalid value
     - Message: Human-readable error description
     - Severity: ERROR, WARNING, or INFO
   
4. **Fix Suggestions**
   - After validation, the system provides fix suggestions
   - These guide you on how to correct the violations

### Creating Custom Shapes

When you select `add`, you can enter custom SHACL shapes in Turtle format:

```turtle
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Your custom shape here
:MyCustomShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :name ;
        sh:minLength 3 ;
        sh:message "Planet names must be at least 3 characters" ;
    ] .
```

After entering your shape:
- Press `Ctrl+Enter` or `Esc, Enter` to submit
- The system will parse and validate your shape
- If valid, it's added to the shapes graph

## Common SHACL Constraints

### Cardinality
```turtle
sh:minCount 1 ;        # At least one value
sh:maxCount 1 ;        # At most one value
```

### Data Types
```turtle
sh:datatype xsd:string ;
sh:datatype xsd:integer ;
sh:datatype xsd:date ;
sh:datatype xsd:boolean ;
```

### Value Ranges
```turtle
sh:minInclusive 0 ;
sh:maxInclusive 100 ;
sh:minExclusive 0 ;
sh:maxExclusive 100 ;
```

### String Patterns
```turtle
sh:pattern "^[A-Z]" ;  # Must start with uppercase
sh:minLength 3 ;
sh:maxLength 50 ;
```

### Node Types
```turtle
sh:nodeKind sh:IRI ;       # Must be an IRI
sh:nodeKind sh:Literal ;   # Must be a literal
sh:nodeKind sh:BlankNode ; # Must be a blank node
```

### Class Constraints
```turtle
sh:class :Planet ;     # Value must be of this class
```

## Validation Results

### Conforming Data
When data conforms to all constraints:
```
✓ VALIDATION PASSED

All data conforms to the SHACL constraints!
```

### Non-Conforming Data
When violations are found:
```
✗ VALIDATION FAILED

Found 3 violation(s):

┌─────────────┬──────────┬────────┬─────────────────────┬──────────┐
│ Focus Node  │ Property │ Value  │ Message             │ Severity │
├─────────────┼──────────┼────────┼─────────────────────┼──────────┤
│ :Mercury    │ :diameter│ 4879   │ Planet diameter...  │ ERROR    │
│ :Venus      │ :name    │        │ Every astronaut...  │ ERROR    │
│ :Apollo11   │ :date    │ "1969" │ Mission launch...   │ ERROR    │
└─────────────┴──────────┴────────┴─────────────────────┴──────────┘

Fix Suggestions:
  1. Consider removing or changing the value '4879' for property :diameter on :Mercury
  2. Add or fix property :name on :Venus
  3. Review the constraint and data
```

## Technical Details

### Architecture

The SHACL mode is built on top of:
- **pyshacl**: W3C-compliant SHACL validator
- **rdflib**: RDF graph manipulation
- **Rich**: Terminal UI formatting

### Components

1. **SHACLEngine** (`engine/shacl_engine.py`)
   - Manages SHACL shapes graph
   - Performs validation using pyshacl
   - Parses and formats violation reports
   - Provides example shapes

2. **Modified Tutorial** (`sparql_tutorial.py`)
   - New `shacl_free_mode()` method
   - Integration with main menu
   - Interactive SHACL commands
   - Violation display and fix suggestions

### Data Flow

```
User Input (SHACL Shape)
    ↓
SHACLEngine.add_shape_from_text()
    ↓
Shapes Graph (rdflib)
    ↓
SHACLEngine.validate()
    ↓
pyshacl validation
    ↓
Violation Reports
    ↓
Terminal Display (Rich)
```

## Advanced Usage

### Programmatic Access

You can also use the SHACL engine programmatically:

```python
from engine.shacl_engine import SHACLEngine

# Initialize
engine = SHACLEngine(data_file="data/knowledge_graph.ttl")

# Add a shape
shape = """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

:MyShape a sh:NodeShape ;
    sh:targetClass :Planet ;
    sh:property [
        sh:path :name ;
        sh:minCount 1 ;
    ] .
"""

success, error = engine.add_shape_from_text(shape)

# Validate
result = engine.validate()
print(f"Conforms: {result['conforms']}")
print(f"Violations: {result['violation_count']}")

for v in result['violations']:
    print(f"  - {v['focus_node']}: {v['message']}")
```

## Educational Value

The SHACL mode teaches you:

1. **Data Quality**: How to define and enforce data quality constraints
2. **RDF Validation**: Industry-standard validation techniques
3. **Constraint Design**: How to write effective SHACL shapes
4. **Error Handling**: How to interpret and fix validation violations
5. **Best Practices**: Common patterns for RDF data validation

## Future Enhancements

Potential improvements for future versions:

- **Auto-fix Functionality**: Automatically correct simple violations
- **Shape Generation**: Generate SHACL shapes from existing data
- **Violation Filtering**: Filter violations by severity or type
- **Shape Templates**: Additional pre-built shape templates
- **Export Results**: Save validation reports to files
- **Interactive Fixes**: Step-by-step wizard for fixing violations
- **Shape Versioning**: Track changes to shapes over time
- **Batch Validation**: Validate multiple datasets at once

## Troubleshooting

### Common Issues

**Q: Shape parsing error**
A: Ensure your shape uses valid Turtle syntax and includes proper prefixes.

**Q: No violations shown but data seems wrong**
A: Check that your shape's `sh:targetClass` matches the class in your data.

**Q: Validation takes a long time**
A: Complex shapes on large datasets can be slow. Consider simplifying shapes or using `abort_on_first` mode.

**Q: Unclear violation messages**
A: Add custom `sh:message` properties to your shapes for clearer error messages.

## References

- [W3C SHACL Specification](https://www.w3.org/TR/shacl/)
- [SHACL Playground](https://shacl.org/playground/)
- [pyshacl Documentation](https://github.com/RDFLib/pySHACL)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)

## License

This SHACL extension maintains the same MIT license as the original SPARQL tutorial.
