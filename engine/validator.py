"""Query validation and hint system for the SPARQL tutorial."""

import re
from typing import Optional


class QueryValidator:
    """Validates user queries and provides hints."""

    def __init__(self):
        self.common_mistakes = [
            {
                "pattern": r"select\s+\*\s+where",
                "fix": "SELECT * WHERE",
                "message": "SPARQL keywords should be uppercase (though lowercase often works too)",
            },
            {
                "pattern": r"\?\w+\s+:\w+\s+:\w+\s*[^.]",
                "check": lambda q: not q.strip().endswith(".") and "}" not in q.split("\n")[-1],
                "message": "Don't forget the period (.) at the end of each triple pattern!",
            },
            {
                "pattern": r"WHERE\s*\{[^}]*$",
                "check": lambda q: q.count("{") > q.count("}"),
                "message": "You have an unclosed brace. Make sure every { has a matching }",
            },
        ]

    def check_query_structure(self, query: str, expected_elements: list = None) -> list:
        """
        Check if a query contains expected structural elements.

        Returns list of missing elements.
        """
        missing = []
        query_upper = query.upper()

        if expected_elements:
            for element in expected_elements:
                if element.upper() not in query_upper:
                    missing.append(element)

        return missing

    def compare_results(self, user_results: list, expected_check: callable) -> tuple:
        """
        Compare user results against expected validation.

        Returns:
            (is_correct: bool, feedback: str)
        """
        try:
            is_correct = expected_check(user_results)
            if is_correct:
                return True, "Your query returned the expected results!"
            else:
                return False, "Your query ran but didn't return the expected results. Try again!"
        except Exception as e:
            return False, f"Could not validate results: {str(e)}"

    def get_structural_hints(self, query: str, solution: str) -> list:
        """
        Compare user query structure with solution and provide hints.
        """
        hints = []
        query_upper = query.upper()
        solution_upper = solution.upper()

        # Check for key SPARQL keywords
        keywords = ["SELECT", "WHERE", "PREFIX", "FILTER", "OPTIONAL", "ORDER BY",
                    "LIMIT", "GROUP BY", "UNION", "BIND", "DISTINCT"]

        for keyword in keywords:
            if keyword in solution_upper and keyword not in query_upper:
                hints.append(f"Consider using {keyword} in your query")

        # Check for specific patterns
        if "rdf:type" in solution.lower() and "rdf:type" not in query.lower() and "a " not in query.lower():
            hints.append("You might need to specify the type using 'rdf:type' or 'a'")

        # Check for variable patterns
        solution_vars = set(re.findall(r'\?(\w+)', solution))
        query_vars = set(re.findall(r'\?(\w+)', query))

        if solution_vars and not query_vars:
            hints.append("Remember to use variables (starting with ?) in your query")

        return hints

    def get_progressive_hint(self, exercise: dict, hint_level: int, user_query: str = "") -> Optional[str]:
        """
        Get a hint based on the level (1-3) and optionally the user's current query.

        Level 1: General direction
        Level 2: More specific guidance
        Level 3: Almost the answer
        """
        hints = exercise.get("hints", [])

        if hint_level <= 0 or hint_level > len(hints):
            return None

        return hints[hint_level - 1]

    def analyze_error(self, error_message: str) -> str:
        """
        Analyze an error message and provide specific guidance.
        """
        error_lower = error_message.lower()

        suggestions = []

        if "prefix" in error_lower:
            suggestions.append(
                "Make sure to declare all prefixes at the top:\n"
                "  PREFIX : <http://space.example.org/>\n"
                "  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
            )

        if "expected" in error_lower and "{" in error_lower:
            suggestions.append(
                "Check your WHERE clause structure:\n"
                "  WHERE {\n"
                "      ?s ?p ?o .\n"
                "  }"
            )

        if "variable" in error_lower:
            suggestions.append(
                "Variables must start with ? or $:\n"
                "  ?name, ?planet, $subject"
            )

        if "aggregate" in error_lower:
            suggestions.append(
                "When using aggregates (COUNT, SUM, etc.):\n"
                "  - Use AS to name results: (COUNT(?x) AS ?count)\n"
                "  - Add GROUP BY for non-aggregated variables"
            )

        if suggestions:
            return "\n\n".join(suggestions)

        return "Review the query syntax and check for typos in keywords and property names."


class HintSystem:
    """Manages hints for exercises."""

    def __init__(self):
        self.hint_counts = {}  # Track hints used per exercise

    def get_hint_count(self, exercise_id: str) -> int:
        """Get number of hints already shown for an exercise."""
        return self.hint_counts.get(exercise_id, 0)

    def increment_hint(self, exercise_id: str) -> int:
        """Increment and return the new hint level."""
        current = self.hint_counts.get(exercise_id, 0)
        self.hint_counts[exercise_id] = current + 1
        return current + 1

    def reset_hints(self, exercise_id: str = None):
        """Reset hint count for an exercise or all exercises."""
        if exercise_id:
            self.hint_counts[exercise_id] = 0
        else:
            self.hint_counts = {}

    def can_show_more_hints(self, exercise_id: str, max_hints: int = 3) -> bool:
        """Check if more hints are available."""
        return self.get_hint_count(exercise_id) < max_hints
