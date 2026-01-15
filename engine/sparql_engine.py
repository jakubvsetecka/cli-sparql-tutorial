"""SPARQL Engine using rdflib for local query execution."""

import os
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.processor import SPARQLResult


class SPARQLEngine:
    """Wrapper around rdflib for executing SPARQL queries."""

    def __init__(self, data_file: str = None):
        """Initialize the SPARQL engine with the knowledge graph."""
        self.graph = Graph()

        # Define namespaces
        self.SPACE = Namespace("http://space.example.org/")
        self.graph.bind("", self.SPACE)
        self.graph.bind("space", self.SPACE)

        # Load the knowledge graph
        if data_file is None:
            # Default to the data file in the project
            data_file = Path(__file__).parent.parent / "data" / "knowledge_graph.ttl"

        if os.path.exists(data_file):
            self.graph.parse(data_file, format="turtle")
            self.triple_count = len(self.graph)
        else:
            raise FileNotFoundError(f"Knowledge graph not found: {data_file}")

    def execute(self, query: str) -> dict:
        """
        Execute a SPARQL query and return results.

        Returns:
            dict with keys:
                - success: bool
                - results: list of dicts (for SELECT)
                - variables: list of variable names
                - result_type: 'SELECT', 'ASK', 'CONSTRUCT', 'DESCRIBE'
                - error: error message if failed
                - raw_result: the raw SPARQLResult object
        """
        try:
            result = self.graph.query(query)

            # Determine result type and format accordingly
            if result.type == "SELECT":
                variables = [str(v) for v in result.vars]
                rows = []
                for row in result:
                    row_dict = {}
                    for var in result.vars:
                        value = row[var]
                        if value is not None:
                            # Clean up the value for display
                            str_value = str(value)
                            # Remove namespace prefixes for readability
                            if str_value.startswith("http://space.example.org/"):
                                str_value = str_value.replace("http://space.example.org/", ":")
                            row_dict[str(var)] = str_value
                        else:
                            row_dict[str(var)] = ""
                    rows.append(row_dict)

                return {
                    "success": True,
                    "results": rows,
                    "variables": variables,
                    "result_type": "SELECT",
                    "count": len(rows),
                    "error": None,
                    "raw_result": result,
                }

            elif result.type == "ASK":
                return {
                    "success": True,
                    "results": [{"result": str(result.askAnswer)}],
                    "variables": ["result"],
                    "result_type": "ASK",
                    "ask_result": result.askAnswer,
                    "error": None,
                    "raw_result": result,
                }

            elif result.type == "CONSTRUCT":
                # For CONSTRUCT, serialize the resulting graph
                constructed = result.graph
                triples = []
                for s, p, o in constructed:
                    triples.append({
                        "subject": str(s),
                        "predicate": str(p),
                        "object": str(o),
                    })

                return {
                    "success": True,
                    "results": triples,
                    "variables": ["subject", "predicate", "object"],
                    "result_type": "CONSTRUCT",
                    "count": len(triples),
                    "error": None,
                    "raw_result": result,
                }

            else:
                # DESCRIBE or other
                return {
                    "success": True,
                    "results": [],
                    "variables": [],
                    "result_type": result.type,
                    "error": None,
                    "raw_result": result,
                }

        except Exception as e:
            error_msg = str(e)
            # Try to provide more helpful error messages
            friendly_error = self._make_error_friendly(error_msg)

            return {
                "success": False,
                "results": [],
                "variables": [],
                "result_type": None,
                "error": friendly_error,
                "raw_error": error_msg,
            }

    def _make_error_friendly(self, error: str) -> str:
        """Convert technical errors to more user-friendly messages."""
        error_lower = error.lower()

        if "expected" in error_lower:
            return f"Syntax Error: {error}\n\nTip: Check your query structure. Common issues:\n  - Missing period at end of triple pattern\n  - Missing closing brace }}\n  - Typo in a keyword (SELECT, WHERE, FILTER, etc.)"

        if "prefix" in error_lower or "unknown namespace" in error_lower:
            return f"Prefix Error: {error}\n\nTip: Make sure you've declared all prefixes at the top of your query:\n  PREFIX : <http://space.example.org/>\n  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"

        if "variable" in error_lower:
            return f"Variable Error: {error}\n\nTip: Variables must start with ? or $, e.g., ?name, ?planet"

        if "aggregate" in error_lower or "group" in error_lower:
            return f"Aggregation Error: {error}\n\nTip: When using COUNT, SUM, etc.:\n  - Non-aggregated variables must be in GROUP BY\n  - Use HAVING (not FILTER) for aggregate conditions"

        return f"Query Error: {error}"

    def validate_query_syntax(self, query: str) -> tuple:
        """
        Check if a query has valid syntax without executing.

        Returns:
            (is_valid: bool, error_message: str or None)
        """
        try:
            prepareQuery(query)
            return True, None
        except Exception as e:
            return False, self._make_error_friendly(str(e))

    def get_stats(self) -> dict:
        """Get statistics about the loaded knowledge graph."""
        # Count entities by type
        stats = {
            "total_triples": len(self.graph),
            "planets": 0,
            "moons": 0,
            "astronauts": 0,
            "missions": 0,
            "agencies": 0,
            "spacecraft": 0,
        }

        type_queries = {
            "planets": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/Planet> }",
            "moons": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/Moon> }",
            "astronauts": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/Astronaut> }",
            "missions": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/Mission> }",
            "agencies": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/SpaceAgency> }",
            "spacecraft": "SELECT (COUNT(?x) AS ?c) WHERE { ?x a <http://space.example.org/Spacecraft> }",
        }

        for key, query in type_queries.items():
            try:
                result = self.graph.query(query)
                for row in result:
                    stats[key] = int(row[0])
            except:
                pass

        return stats
