"""Lesson content for the SPARQL tutorial."""

LESSONS = [
    # =========================================================================
    # LESSON 1: Introduction to SPARQL and RDF
    # =========================================================================
    {
        "id": 1,
        "title": "Introduction to SPARQL and RDF",
        "category": "Beginner",
        "concept": """
## What is SPARQL?

**SPARQL** (pronounced "sparkle") stands for **SPARQL Protocol and RDF Query Language**.
It's the standard query language for retrieving and manipulating data stored in RDF format.

Think of SPARQL as SQL for graph databases!

## What is RDF?

**RDF** (Resource Description Framework) stores data as a graph of connected facts.
Each fact is a **triple** consisting of three parts:

```
Subject  →  Predicate  →  Object
```

For example:
- `Mars` → `hasType` → `Planet`
- `Neil Armstrong` → `walkedOn` → `Moon`
- `Apollo 11` → `launchDate` → `1969-07-16`

## Our Dataset: Space Exploration

In this tutorial, we'll explore a knowledge graph about space! It contains:

- **Planets**: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
- **Moons**: The Moon, Phobos, Europa, Titan, and more
- **Astronauts**: Neil Armstrong, Yuri Gagarin, Sally Ride...
- **Missions**: Apollo 11, Voyager 1, Curiosity Rover...
- **Space Agencies**: NASA, ESA, SpaceX, Roscosmos...

Let's start exploring! 🚀
""",
        "exercises": [
            {
                "task": """This is an introductory lesson. Copy and paste this complete query to see some data:

    SELECT * WHERE { ?s ?p ?o } LIMIT 5

This retrieves 5 random facts (triples) from our space knowledge graph!""",
                "hints": [
                    "Copy the entire query: SELECT * WHERE { ?s ?p ?o } LIMIT 5",
                    "Make sure to include WHERE { } - this is required in SPARQL",
                    "The ?s ?p ?o are variables that match any Subject, Predicate, Object",
                ],
                "solution": "SELECT * WHERE { ?s ?p ?o } LIMIT 5",
                "validate": lambda results: len(results) > 0,
                "success_message": "Welcome to SPARQL! You just ran your first query and retrieved data from the knowledge graph!",
            }
        ],
    },

    # =========================================================================
    # LESSON 2: Basic SELECT Queries
    # =========================================================================
    {
        "id": 2,
        "title": "Basic SELECT Queries",
        "category": "Beginner",
        "concept": """
## The SELECT Statement

The most basic SPARQL query uses `SELECT` to retrieve data. The structure is:

```sparql
SELECT ?variable1 ?variable2 ...
WHERE {
    # triple patterns go here
}
```

## Variables in SPARQL

Variables start with `?` or `$` (we'll use `?`):
- `?name` - a variable called "name"
- `?planet` - a variable called "planet"

## Prefixes

URIs can be long, so we use **prefixes** as shortcuts:

```sparql
PREFIX : <http://space.example.org/>

SELECT ?name
WHERE { ... }
```

The prefix `:` is a shorthand for our space ontology.

## Your First Real Query

To find all planets, we match things that have `rdf:type` equal to `:Planet`:

```sparql
PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?planet
WHERE {
    ?planet rdf:type :Planet .
}
```
""",
        "exercises": [
            {
                "task": "Write a query to SELECT all astronauts. Use `?astronaut` as your variable and match where `rdf:type` is `:Astronaut`.",
                "hints": [
                    "Start with PREFIX declarations for `:` and `rdf:`",
                    "Use the pattern: ?astronaut rdf:type :Astronaut .",
                    "Don't forget the period at the end of the triple pattern!",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?astronaut
WHERE {
    ?astronaut rdf:type :Astronaut .
}""",
                "validate": lambda results: len(results) >= 10,
                "success_message": "Excellent! You found all the astronauts in our database!",
            }
        ],
    },

    # =========================================================================
    # LESSON 3: Triple Patterns
    # =========================================================================
    {
        "id": 3,
        "title": "Triple Patterns - Subject, Predicate, Object",
        "category": "Beginner",
        "concept": """
## Understanding Triple Patterns

Every piece of data in RDF is stored as a triple:

```
Subject  --[Predicate]-->  Object
```

In SPARQL, we write patterns to match these triples:

```sparql
?subject :predicate ?object .
```

## Reading the Pattern

Let's decode this pattern:
```sparql
?planet :name ?planetName .
```

This matches triples where:
- **Subject**: Any resource (we capture it in `?planet`)
- **Predicate**: The `:name` property
- **Object**: Any value (we capture it in `?planetName`)

## Concrete Values

You can also use concrete values:

```sparql
:Earth :name ?earthName .
```

This finds the name of specifically Earth.

## Example Query

```sparql
PREFIX : <http://space.example.org/>

SELECT ?planet ?name
WHERE {
    ?planet :name ?name .
}
```

This retrieves anything that has a `:name` property!
""",
        "exercises": [
            {
                "task": "Write a query to find the names of all Space Agencies. Select both `?agency` and `?name`. Match agencies using `rdf:type :SpaceAgency` and get their names with `:name`.",
                "hints": [
                    "You need TWO triple patterns in the WHERE clause",
                    "First pattern: ?agency rdf:type :SpaceAgency .",
                    "Second pattern: ?agency :name ?name .",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?agency ?name
WHERE {
    ?agency rdf:type :SpaceAgency .
    ?agency :name ?name .
}""",
                "validate": lambda results: len(results) >= 5 and any('NASA' in str(r) for r in results),
                "success_message": "Great work! You've mastered triple patterns!",
            }
        ],
    },

    # =========================================================================
    # LESSON 4: Multiple Patterns and Joins
    # =========================================================================
    {
        "id": 4,
        "title": "Multiple Patterns and Joins",
        "category": "Beginner",
        "concept": """
## Joining Patterns Together

The real power of SPARQL comes from combining multiple patterns.
When you use the same variable in multiple patterns, SPARQL **joins** them.

## How Joins Work

```sparql
?mission :destination ?planet .
?planet :name ?planetName .
```

Here, `?planet` appears in both patterns, so:
1. First, find all mission destinations
2. Then, find the names of those destinations
3. Return only matches where the planet in both is the same

## Example: Missions and Their Destinations

```sparql
PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?missionName ?planetName
WHERE {
    ?mission rdf:type :Mission .
    ?mission :name ?missionName .
    ?mission :destination ?planet .
    ?planet :name ?planetName .
}
```

This query:
1. Finds all missions
2. Gets each mission's name
3. Gets each mission's destination
4. Gets the name of that destination

## Note on Pattern Order

Pattern order doesn't change results, but can affect performance.
Put more specific patterns first when possible.
""",
        "exercises": [
            {
                "task": "Write a query to find all astronauts who walked on the Moon. Select their names. Use the `:walkedOnMoon` property (it's `true` for moonwalkers).",
                "hints": [
                    "Match astronauts: ?astro rdf:type :Astronaut .",
                    "Filter for moonwalkers: ?astro :walkedOnMoon true .",
                    "Get their names: ?astro :name ?name .",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name
WHERE {
    ?astro rdf:type :Astronaut .
    ?astro :walkedOnMoon true .
    ?astro :name ?name .
}""",
                "validate": lambda results: len(results) >= 4 and any('Neil Armstrong' in str(r) or 'Buzz Aldrin' in str(r) for r in results),
                "success_message": "Perfect! You found the moonwalkers! 🌙",
            }
        ],
    },

    # =========================================================================
    # LESSON 5: FILTER - Constraining Results
    # =========================================================================
    {
        "id": 5,
        "title": "FILTER - Constraining Results",
        "category": "Beginner",
        "concept": """
## The FILTER Clause

`FILTER` lets you add conditions to constrain your results.
It works like a WHERE clause in SQL.

## Basic Syntax

```sparql
SELECT ?x
WHERE {
    ?x :property ?value .
    FILTER (condition)
}
```

## Common Filter Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| Equals | `=` | `FILTER (?x = 10)` |
| Not equals | `!=` | `FILTER (?x != 10)` |
| Greater than | `>` | `FILTER (?x > 10)` |
| Less than | `<` | `FILTER (?x < 10)` |
| String contains | `CONTAINS()` | `FILTER (CONTAINS(?name, "Apollo"))` |
| Regex | `REGEX()` | `FILTER (REGEX(?name, "^A"))` |
| Logical AND | `&&` | `FILTER (?x > 5 && ?x < 10)` |
| Logical OR | `||` | `FILTER (?x < 5 || ?x > 10)` |

## Example: Large Planets

```sparql
PREFIX : <http://space.example.org/>

SELECT ?name ?diameter
WHERE {
    ?planet :name ?name .
    ?planet :diameter ?diameter .
    FILTER (?diameter > 50000)
}
```

This finds planets with diameter greater than 50,000 km.
""",
        "exercises": [
            {
                "task": "Find all planets that have more than 10 moons. Select the planet name and number of moons. Use `:numberOfMoons` property and `FILTER`.",
                "hints": [
                    "Get planets with: ?planet rdf:type :Planet .",
                    "Get moon count with: ?planet :numberOfMoons ?moons .",
                    "Add: FILTER (?moons > 10)",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?moons
WHERE {
    ?planet rdf:type :Planet .
    ?planet :name ?name .
    ?planet :numberOfMoons ?moons .
    FILTER (?moons > 10)
}""",
                "validate": lambda results: len(results) >= 4,
                "success_message": "Excellent filtering! You found the planets with many moons! 🌟",
            }
        ],
    },

    # =========================================================================
    # LESSON 6: OPTIONAL Patterns
    # =========================================================================
    {
        "id": 6,
        "title": "OPTIONAL - Handling Missing Data",
        "category": "Beginner",
        "concept": """
## The OPTIONAL Clause

Sometimes data is incomplete. `OPTIONAL` lets you match patterns
that might not exist for every result.

## Without OPTIONAL

```sparql
SELECT ?name ?headquarters
WHERE {
    ?agency :name ?name .
    ?agency :headquarters ?headquarters .
}
```

This only returns agencies that HAVE headquarters defined.

## With OPTIONAL

```sparql
SELECT ?name ?headquarters
WHERE {
    ?agency :name ?name .
    OPTIONAL { ?agency :headquarters ?headquarters . }
}
```

This returns ALL agencies, with `headquarters` being empty if not defined.

## Real-World Example

Our missions might or might not have crew members:

```sparql
PREFIX : <http://space.example.org/>

SELECT ?missionName ?astronaut
WHERE {
    ?mission :name ?missionName .
    OPTIONAL { ?mission :crewMember ?astronaut . }
}
```

Uncrewed missions (like Voyager) will still appear, but with no astronaut.

## Multiple OPTIONALs

You can have multiple OPTIONAL blocks:

```sparql
OPTIONAL { ?x :prop1 ?val1 . }
OPTIONAL { ?x :prop2 ?val2 . }
```
""",
        "exercises": [
            {
                "task": "Write a query to get all missions with their names and OPTIONALLY their launch dates. Some missions might not have dates recorded. Select `?name` and `?date`.",
                "hints": [
                    "Start by matching: ?mission rdf:type :Mission .",
                    "Get name: ?mission :name ?name .",
                    "Use OPTIONAL for date: OPTIONAL { ?mission :launchDate ?date . }",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?date
WHERE {
    ?mission rdf:type :Mission .
    ?mission :name ?name .
    OPTIONAL { ?mission :launchDate ?date . }
}""",
                "validate": lambda results: len(results) >= 10,
                "success_message": "Great job! OPTIONAL is very useful for real-world data! 📅",
            }
        ],
    },

    # =========================================================================
    # LESSON 7: ORDER BY and LIMIT
    # =========================================================================
    {
        "id": 7,
        "title": "ORDER BY and LIMIT",
        "category": "Beginner",
        "concept": """
## Sorting Results with ORDER BY

Use `ORDER BY` to sort your results:

```sparql
SELECT ?name ?diameter
WHERE {
    ?planet :name ?name .
    ?planet :diameter ?diameter .
}
ORDER BY ?diameter
```

## Sorting Options

| Syntax | Effect |
|--------|--------|
| `ORDER BY ?x` | Ascending order (smallest first) |
| `ORDER BY ASC(?x)` | Ascending order (explicit) |
| `ORDER BY DESC(?x)` | Descending order (largest first) |

## Multiple Sort Keys

```sparql
ORDER BY ?category DESC(?date)
```

Sort by category first, then by date descending within each category.

## Limiting Results with LIMIT

`LIMIT` restricts the number of results:

```sparql
SELECT ?name
WHERE { ... }
LIMIT 10
```

## OFFSET for Pagination

Skip the first N results:

```sparql
SELECT ?name
WHERE { ... }
LIMIT 10
OFFSET 20
```

This skips 20 results, then returns the next 10.

## Example: Top 3 Largest Planets

```sparql
PREFIX : <http://space.example.org/>

SELECT ?name ?diameter
WHERE {
    ?planet :name ?name .
    ?planet :diameter ?diameter .
}
ORDER BY DESC(?diameter)
LIMIT 3
```
""",
        "exercises": [
            {
                "task": "Find the 5 oldest astronauts (by birth year). Select their name and birth year, ordered by birth year ascending (oldest first).",
                "hints": [
                    "Match astronauts with rdf:type :Astronaut",
                    "Get :name and :birthYear properties",
                    "Use ORDER BY ?birthYear (ascending is default)",
                    "Add LIMIT 5 at the end",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?birthYear
WHERE {
    ?astro rdf:type :Astronaut .
    ?astro :name ?name .
    ?astro :birthYear ?birthYear .
}
ORDER BY ?birthYear
LIMIT 5""",
                "validate": lambda results: len(results) == 5,
                "success_message": "Perfect! You can now sort and limit results! 🎯",
            }
        ],
    },

    # =========================================================================
    # LESSON 8: DISTINCT - Removing Duplicates
    # =========================================================================
    {
        "id": 8,
        "title": "DISTINCT - Removing Duplicates",
        "category": "Intermediate",
        "concept": """
## Why Duplicates Occur

When joining data, you might get duplicate rows.

For example, if an astronaut was on multiple missions:
```
Neil Armstrong | Apollo 11
Neil Armstrong | Gemini 8
```

If you only select the astronaut name, you'd get "Neil Armstrong" twice.

## Using DISTINCT

`DISTINCT` removes duplicate rows:

```sparql
SELECT DISTINCT ?name
WHERE {
    ?mission :crewMember ?astro .
    ?astro :name ?name .
}
```

Now each astronaut appears only once, even if they flew multiple missions.

## DISTINCT vs REDUCED

- `DISTINCT` guarantees no duplicates (slower, must check all)
- `REDUCED` allows but doesn't guarantee duplicates removed (faster)

For most cases, use `DISTINCT`.

## Example: Unique Mission Types

```sparql
PREFIX : <http://space.example.org/>

SELECT DISTINCT ?missionType
WHERE {
    ?mission :missionType ?missionType .
}
```

This lists each mission type only once.
""",
        "exercises": [
            {
                "task": "Find all DISTINCT nationalities of astronauts in the database. Each nationality should appear only once.",
                "hints": [
                    "Use SELECT DISTINCT ?nationality",
                    "Match astronauts: ?astro rdf:type :Astronaut .",
                    "Get nationality: ?astro :nationality ?nationality .",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?nationality
WHERE {
    ?astro rdf:type :Astronaut .
    ?astro :nationality ?nationality .
}""",
                "validate": lambda results: len(results) >= 3 and len(results) == len(set(str(r) for r in results)),
                "success_message": "Excellent! DISTINCT is great for getting unique values! 🌍",
            }
        ],
    },

    # =========================================================================
    # LESSON 9: COUNT and GROUP BY
    # =========================================================================
    {
        "id": 9,
        "title": "COUNT and GROUP BY - Aggregations",
        "category": "Intermediate",
        "concept": """
## Aggregate Functions

SPARQL supports aggregation functions:

| Function | Description |
|----------|-------------|
| `COUNT(?x)` | Count number of values |
| `SUM(?x)` | Sum of numeric values |
| `AVG(?x)` | Average of numeric values |
| `MIN(?x)` | Minimum value |
| `MAX(?x)` | Maximum value |

## Basic COUNT

```sparql
SELECT (COUNT(?planet) AS ?total)
WHERE {
    ?planet rdf:type :Planet .
}
```

The `AS ?total` gives the count a name.

## GROUP BY

To count items per group, use `GROUP BY`:

```sparql
SELECT ?nationality (COUNT(?astro) AS ?count)
WHERE {
    ?astro :nationality ?nationality .
}
GROUP BY ?nationality
```

This counts astronauts per nationality.

## HAVING - Filter Groups

`HAVING` filters groups (like FILTER but for aggregates):

```sparql
SELECT ?agency (COUNT(?mission) AS ?missionCount)
WHERE {
    ?mission :launchedBy ?agency .
}
GROUP BY ?agency
HAVING (COUNT(?mission) > 2)
```

Only shows agencies with more than 2 missions.

## Important Rules

1. Every non-aggregated variable must be in GROUP BY
2. You can't use FILTER on aggregated values (use HAVING)
""",
        "exercises": [
            {
                "task": "Count how many missions each space agency has launched. Select the agency name and the count. Order by count descending.",
                "hints": [
                    "Get agency name: ?agency :name ?agencyName .",
                    "Link to missions: ?mission :launchedBy ?agency .",
                    "Use: SELECT ?agencyName (COUNT(?mission) AS ?count)",
                    "Add GROUP BY ?agencyName and ORDER BY DESC(?count)",
                ],
                "solution": """PREFIX : <http://space.example.org/>

SELECT ?agencyName (COUNT(?mission) AS ?count)
WHERE {
    ?agency :name ?agencyName .
    ?mission :launchedBy ?agency .
}
GROUP BY ?agencyName
ORDER BY DESC(?count)""",
                "validate": lambda results: len(results) >= 3,
                "success_message": "Amazing! Aggregations are powerful for data analysis! 📊",
            }
        ],
    },

    # =========================================================================
    # LESSON 10: UNION - Combining Patterns
    # =========================================================================
    {
        "id": 10,
        "title": "UNION - Combining Patterns",
        "category": "Intermediate",
        "concept": """
## The UNION Operator

`UNION` combines results from different patterns (like SQL's UNION).

## Basic Syntax

```sparql
SELECT ?name
WHERE {
    { ?x rdf:type :Planet . ?x :name ?name . }
    UNION
    { ?x rdf:type :Moon . ?x :name ?name . }
}
```

This returns both planet names AND moon names.

## When to Use UNION

Use UNION when you want:
- Results matching Pattern A **OR** Pattern B
- To combine different types of entities
- Alternative ways to find related data

## Multiple UNIONs

```sparql
{ pattern1 }
UNION
{ pattern2 }
UNION
{ pattern3 }
```

## UNION vs Multiple Patterns

These are different:

```sparql
# AND - must match BOTH patterns
?x :prop1 ?val1 .
?x :prop2 ?val2 .

# OR - must match EITHER pattern (using UNION)
{ ?x :prop1 ?val1 . }
UNION
{ ?x :prop2 ?val2 . }
```

## Adding a Type Column

To know which pattern matched:

```sparql
SELECT ?name ?type
WHERE {
    { ?x rdf:type :Planet . ?x :name ?name . BIND("Planet" AS ?type) }
    UNION
    { ?x rdf:type :Moon . ?x :name ?name . BIND("Moon" AS ?type) }
}
```
""",
        "exercises": [
            {
                "task": "Write a query that finds names of both Planets AND Moons using UNION. Select the name and use BIND to add a ?type column indicating 'Planet' or 'Moon'.",
                "hints": [
                    "Use two blocks: one for planets, one for moons",
                    "Each block should get rdf:type and :name",
                    "Use BIND(\"Planet\" AS ?type) in the planet block",
                    "Connect them with UNION",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?type
WHERE {
    { ?x rdf:type :Planet . ?x :name ?name . BIND("Planet" AS ?type) }
    UNION
    { ?x rdf:type :Moon . ?x :name ?name . BIND("Moon" AS ?type) }
}""",
                "validate": lambda results: len(results) >= 15,
                "success_message": "Excellent! UNION is great for combining different data types! 🔗",
            }
        ],
    },

    # =========================================================================
    # LESSON 11: BIND and Expressions
    # =========================================================================
    {
        "id": 11,
        "title": "BIND and Expressions - Computed Values",
        "category": "Intermediate",
        "concept": """
## The BIND Clause

`BIND` creates new variables from expressions:

```sparql
BIND (expression AS ?newVariable)
```

## Simple Calculations

```sparql
SELECT ?name ?diameter ?radius
WHERE {
    ?planet :name ?name .
    ?planet :diameter ?diameter .
    BIND (?diameter / 2 AS ?radius)
}
```

## String Functions

| Function | Example |
|----------|---------|
| `CONCAT()` | `CONCAT(?first, " ", ?last)` |
| `STRLEN()` | `STRLEN(?name)` |
| `UCASE()` | `UCASE(?name)` - uppercase |
| `LCASE()` | `LCASE(?name)` - lowercase |
| `SUBSTR()` | `SUBSTR(?name, 1, 3)` - first 3 chars |
| `STR()` | Convert to string |

## Conditional Expressions with IF

```sparql
BIND (IF(?diameter > 50000, "Large", "Small") AS ?size)
```

## Math Functions

| Function | Description |
|----------|-------------|
| `ABS()` | Absolute value |
| `ROUND()` | Round to nearest integer |
| `CEIL()` | Round up |
| `FLOOR()` | Round down |

## Example: Categorizing Planets

```sparql
PREFIX : <http://space.example.org/>

SELECT ?name ?diameter ?category
WHERE {
    ?planet :name ?name .
    ?planet :diameter ?diameter .
    BIND (IF(?diameter > 50000, "Gas Giant",
          IF(?diameter > 10000, "Terrestrial", "Dwarf")) AS ?category)
}
```
""",
        "exercises": [
            {
                "task": "Calculate the radius of each planet (diameter / 2) and add a size category: 'Giant' if diameter > 50000, otherwise 'Rocky'. Select name, diameter, radius, and category.",
                "hints": [
                    "Use BIND (?diameter / 2 AS ?radius)",
                    "Use BIND with IF for category: BIND(IF(?diameter > 50000, \"Giant\", \"Rocky\") AS ?category)",
                    "Select ?name, ?diameter, ?radius, ?category",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?diameter ?radius ?category
WHERE {
    ?planet rdf:type :Planet .
    ?planet :name ?name .
    ?planet :diameter ?diameter .
    BIND (?diameter / 2 AS ?radius)
    BIND (IF(?diameter > 50000, "Giant", "Rocky") AS ?category)
}""",
                "validate": lambda results: len(results) == 8 and any('radius' in str(r).lower() or isinstance(r, dict) for r in results),
                "success_message": "Great work with computed values! You're becoming a SPARQL expert! 🧮",
            }
        ],
    },

    # =========================================================================
    # LESSON 12: Subqueries
    # =========================================================================
    {
        "id": 12,
        "title": "Subqueries - Nested Queries",
        "category": "Advanced",
        "concept": """
## What are Subqueries?

Subqueries are queries inside other queries. They're useful for:
- Pre-filtering data
- Computing intermediate results
- Complex aggregations

## Basic Syntax

```sparql
SELECT ?name ?avgMoons
WHERE {
    ?planet :name ?name .
    {
        SELECT (AVG(?moons) AS ?avgMoons)
        WHERE {
            ?p :numberOfMoons ?moons .
        }
    }
}
```

## Common Use Cases

### 1. Find Above Average

```sparql
SELECT ?name ?moons
WHERE {
    ?planet :name ?name .
    ?planet :numberOfMoons ?moons .
    {
        SELECT (AVG(?m) AS ?avg)
        WHERE { ?p :numberOfMoons ?m . }
    }
    FILTER (?moons > ?avg)
}
```

### 2. Top N Per Group

```sparql
SELECT ?agency ?missionName
WHERE {
    ?agency :name ?agencyName .
    {
        SELECT ?agency (MAX(?date) AS ?latestDate)
        WHERE { ?m :launchedBy ?agency . ?m :launchDate ?date . }
        GROUP BY ?agency
    }
    ?mission :launchedBy ?agency .
    ?mission :launchDate ?latestDate .
    ?mission :name ?missionName .
}
```

## Important Notes

- Subquery variables are only visible if SELECTed
- Subqueries execute first, then outer query uses results
- Keep subqueries simple for readability
""",
        "exercises": [
            {
                "task": "Find planets with more moons than the average. Use a subquery to calculate the average number of moons, then filter planets above that average.",
                "hints": [
                    "Inner query: SELECT (AVG(?m) AS ?avg) WHERE { ?p :numberOfMoons ?m . }",
                    "Outer query: Get planet name and moon count",
                    "Add FILTER (?moons > ?avg) after the subquery",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?moons
WHERE {
    ?planet rdf:type :Planet .
    ?planet :name ?name .
    ?planet :numberOfMoons ?moons .
    {
        SELECT (AVG(?m) AS ?avg)
        WHERE {
            ?p :numberOfMoons ?m .
        }
    }
    FILTER (?moons > ?avg)
}""",
                "validate": lambda results: len(results) >= 2 and len(results) <= 5,
                "success_message": "Incredible! Subqueries are advanced SPARQL! 🏆",
            }
        ],
    },

    # =========================================================================
    # LESSON 13: Property Paths
    # =========================================================================
    {
        "id": 13,
        "title": "Property Paths - Following Relationships",
        "category": "Advanced",
        "concept": """
## What are Property Paths?

Property paths let you traverse multiple relationships in one pattern.
Think of it as following a path through the graph.

## Path Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `/` | Sequence | `:A/:B` - A then B |
| `|` | Alternative | `:A|:B` - A or B |
| `*` | Zero or more | `:A*` - any number of A |
| `+` | One or more | `:A+` - at least one A |
| `?` | Zero or one | `:A?` - optional A |
| `^` | Inverse | `^:A` - reverse direction |

## Examples

### Sequence Path
```sparql
?mission :destination/:name ?destName .
```
Equivalent to:
```sparql
?mission :destination ?dest .
?dest :name ?destName .
```

### Alternative Path
```sparql
?x :name|rdfs:label ?label .
```
Matches either `:name` or `rdfs:label`.

### Transitive Path
```sparql
?x :subClassOf+ :Thing .
```
Finds all ancestors (one or more steps).

### Inverse Path
```sparql
?moon ^:orbits ?planet .
```
Same as: `?planet :orbits ?moon .` (reversed direction)

## Real Example: Find What Moons Orbit

```sparql
PREFIX : <http://space.example.org/>

SELECT ?moonName ?planetName
WHERE {
    ?moon :orbits/:name ?planetName .
    ?moon :name ?moonName .
}
```
""",
        "exercises": [
            {
                "task": "Use a property path to find mission names and the names of planets they visited in one pattern. Use `:destination/:name` as a path.",
                "hints": [
                    "Use the path: ?mission :destination/:name ?planetName",
                    "This follows :destination then :name in one pattern",
                    "Also get the mission name: ?mission :name ?missionName",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?missionName ?planetName
WHERE {
    ?mission rdf:type :Mission .
    ?mission :name ?missionName .
    ?mission :destination/:name ?planetName .
}""",
                "validate": lambda results: len(results) >= 5,
                "success_message": "Property paths are elegant! You're mastering advanced SPARQL! ⛓️",
            }
        ],
    },

    # =========================================================================
    # LESSON 14: CONSTRUCT - Building Graphs
    # =========================================================================
    {
        "id": 14,
        "title": "CONSTRUCT - Building New Graphs",
        "category": "Advanced",
        "concept": """
## Beyond SELECT: CONSTRUCT

While `SELECT` returns a table, `CONSTRUCT` returns a new RDF graph!

## Basic Syntax

```sparql
CONSTRUCT {
    ?s ?p ?o .
}
WHERE {
    ?s ?p ?o .
}
```

## Why Use CONSTRUCT?

1. **Transform data** - reshape RDF into different structures
2. **Create summaries** - build simplified graphs
3. **Data integration** - combine data from multiple sources
4. **Export subsets** - extract specific portions of a graph

## Example: Create a Simplified Graph

```sparql
PREFIX : <http://space.example.org/>

CONSTRUCT {
    ?planet :planetName ?name .
    ?planet :moonCount ?moons .
}
WHERE {
    ?planet rdf:type :Planet .
    ?planet :name ?name .
    ?planet :numberOfMoons ?moons .
}
```

This creates new triples with renamed properties.

## Creating New Relationships

```sparql
CONSTRUCT {
    ?astro :visitedBody ?dest .
}
WHERE {
    ?mission :crewMember ?astro .
    ?mission :destination ?dest .
}
```

This infers new relationships that weren't explicit!

## Output Format

CONSTRUCT returns valid RDF (often in Turtle or N-Triples format).
It's useful for data pipelines and transformations.
""",
        "exercises": [
            {
                "task": "Use CONSTRUCT to create a simplified graph where each astronaut has a `:fullName` property (their name) and `:bornIn` property (their birth year). Transform the data from our existing properties.",
                "hints": [
                    "CONSTRUCT { ?astro :fullName ?name . ?astro :bornIn ?year . }",
                    "In WHERE, match astronauts and get :name and :birthYear",
                    "The CONSTRUCT creates new property names",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
    ?astro :fullName ?name .
    ?astro :bornIn ?year .
}
WHERE {
    ?astro rdf:type :Astronaut .
    ?astro :name ?name .
    ?astro :birthYear ?year .
}""",
                "validate": lambda results: True,  # CONSTRUCT validation is different
                "success_message": "Excellent! CONSTRUCT is powerful for data transformation! 🔨",
            }
        ],
    },

    # =========================================================================
    # LESSON 15: ASK and DESCRIBE
    # =========================================================================
    {
        "id": 15,
        "title": "ASK and DESCRIBE Queries",
        "category": "Advanced",
        "concept": """
## ASK Queries

`ASK` returns true/false - does any data match the pattern?

```sparql
ASK {
    ?planet :name "Earth" .
}
```

Returns: `true` or `false`

## When to Use ASK

- Checking if data exists
- Validation queries
- Conditional logic in applications

## Examples

```sparql
# Is there a planet named Pluto?
ASK { ?x :name "Pluto" . ?x rdf:type :Planet . }

# Did any mission visit Mars?
ASK { ?m :destination :Mars . }

# Are there astronauts born before 1930?
ASK { ?a :birthYear ?y . FILTER (?y < 1930) }
```

## DESCRIBE Queries

`DESCRIBE` returns all known information about a resource:

```sparql
DESCRIBE :Mars
```

This returns every triple where `:Mars` is the subject or object.

## DESCRIBE with Patterns

```sparql
DESCRIBE ?planet
WHERE {
    ?planet :numberOfMoons ?moons .
    FILTER (?moons > 50)
}
```

Describes all planets with more than 50 moons.

## Query Form Summary

| Form | Returns | Use For |
|------|---------|---------|
| `SELECT` | Table of values | Most queries |
| `CONSTRUCT` | New RDF graph | Data transformation |
| `ASK` | Boolean | Existence checks |
| `DESCRIBE` | RDF about resource | Exploration |
""",
        "exercises": [
            {
                "task": "Write an ASK query to check if there are any missions that were NOT successful (`:successful` is `false`).",
                "hints": [
                    "Use ASK { ... } instead of SELECT",
                    "Match: ?mission rdf:type :Mission .",
                    "Add: ?mission :successful false .",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

ASK {
    ?mission rdf:type :Mission .
    ?mission :successful false .
}""",
                "validate": lambda results: True,  # ASK returns boolean
                "success_message": "Perfect! You know all four SPARQL query forms! 🎓",
            }
        ],
    },

    # =========================================================================
    # LESSON 16: Final Challenge
    # =========================================================================
    {
        "id": 16,
        "title": "Final Challenge - Putting It All Together",
        "category": "Advanced",
        "concept": """
## Congratulations, Space Explorer! 🚀

You've learned all the major SPARQL concepts:

### Beginner
- ✓ SELECT queries and variables
- ✓ Triple patterns (Subject-Predicate-Object)
- ✓ Multiple patterns and joins
- ✓ FILTER for conditions
- ✓ OPTIONAL for missing data
- ✓ ORDER BY and LIMIT

### Intermediate
- ✓ DISTINCT for unique values
- ✓ COUNT, GROUP BY, and aggregations
- ✓ UNION for combining patterns
- ✓ BIND for computed values

### Advanced
- ✓ Subqueries
- ✓ Property paths
- ✓ CONSTRUCT, ASK, DESCRIBE

## The Final Challenge

Now it's time to combine these skills!

Your mission: Write a comprehensive query that finds:
- American astronauts who walked on the Moon
- Include their name and birth year
- Order by birth year
- Show only the name and a computed column showing how old they were in 1969

This requires: SELECT, triple patterns, FILTER, BIND, and ORDER BY!
""",
        "exercises": [
            {
                "task": "Find American moonwalkers, calculate their age in 1969 (the year of Apollo 11), and sort by birth year. Select name and ageIn1969.",
                "hints": [
                    "Filter for :nationality 'American' and :walkedOnMoon true",
                    "Get :name and :birthYear",
                    "Use BIND(1969 - ?birthYear AS ?ageIn1969)",
                    "ORDER BY ?birthYear",
                ],
                "solution": """PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?name ?ageIn1969
WHERE {
    ?astro rdf:type :Astronaut .
    ?astro :name ?name .
    ?astro :nationality "American" .
    ?astro :walkedOnMoon true .
    ?astro :birthYear ?birthYear .
    BIND(1969 - ?birthYear AS ?ageIn1969)
}
ORDER BY ?birthYear""",
                "validate": lambda results: len(results) >= 3,
                "success_message": "🏆 CONGRATULATIONS! You've completed the SPARQL Tutorial! You are now a SPARQL Master! 🏆",
            }
        ],
    },
]

# Data description for showing available data
DATA_DESCRIPTION = """
## Space Exploration Knowledge Graph

### Entities Available:

**Planets** (8 total)
- Properties: `name`, `diameter` (km), `distanceFromSun` (million km), `numberOfMoons`, `hasRings`

**Moons** (10 total)
- Properties: `name`, `diameter`, `orbits` (which planet)

**Astronauts** (12 total)
- Properties: `name`, `nationality`, `birthYear`, `firstSpaceFlight`, `walkedOnMoon`

**Space Agencies** (6 total)
- Properties: `name`, `founded` (year), `headquarters`

**Missions** (13 total)
- Properties: `name`, `launchDate`, `launchedBy`, `destination`, `crewMember`, `usedSpacecraft`, `missionType`, `successful`

**Spacecraft** (7 total)
- Properties: `name`

### Prefixes:
```sparql
PREFIX : <http://space.example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```
"""
