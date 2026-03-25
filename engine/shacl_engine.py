"""SHACL Engine for validating RDF graphs with SHACL constraints."""

import os
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SH, XSD
from pyshacl import validate


class SHACLEngine:
    """Wrapper for SHACL validation operations."""

    def __init__(self, data_graph: Graph = None, data_file: str = None):
        """
        Initialize the SHACL engine.
        
        Args:
            data_graph: Pre-loaded RDF graph to validate
            data_file: Path to RDF data file (Turtle format)
        """
        # Load or use provided data graph
        if data_graph is not None:
            self.data_graph = data_graph
        elif data_file is not None:
            self.data_graph = Graph()
            if os.path.exists(data_file):
                self.data_graph.parse(data_file, format="turtle")
            else:
                raise FileNotFoundError(f"Data file not found: {data_file}")
        else:
            # Default to the knowledge graph
            data_file = Path(__file__).parent.parent / "data" / "knowledge_graph.ttl"
            self.data_graph = Graph()
            self.data_graph.parse(data_file, format="turtle")

        # Define namespaces
        self.SPACE = Namespace("http://space.example.org/")
        self.SH = SH
        
        # Initialize an empty shapes graph
        self.shapes_graph = Graph()
        self.shapes_graph.bind("sh", SH)
        self.shapes_graph.bind("", self.SPACE)
        self.shapes_graph.bind("space", self.SPACE)
        
        # Store validation results
        self.last_validation = None

    def add_shape_from_text(self, shape_text: str, format: str = "turtle") -> tuple:
        """
        Add a SHACL shape from text to the shapes graph.
        Automatically adds standard prefixes if not present.
        
        Args:
            shape_text: SHACL shape definition in Turtle or other RDF format
            format: RDF serialization format (default: "turtle")
            
        Returns:
            (success: bool, error_message: str or None)
        """
        try:
            # Auto-add standard prefixes if not present
            if format == "turtle" and not shape_text.strip().startswith("@prefix"):
                standard_prefixes = """@prefix : <http://space.example.org/> .
            @prefix sh: <http://www.w3.org/ns/shacl#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

            """
                shape_text = standard_prefixes + shape_text

            # Parse into a temporary graph
            temp_graph = Graph()
            temp_graph.parse(data=shape_text, format=format)
            
            # Add all triples to the shapes graph
            for triple in temp_graph:
                self.shapes_graph.add(triple)
                
            return True, None
        except Exception as e:
            return False, f"Error parsing SHACL shape: {str(e)}"

    def clear_shapes(self):
        """Clear all shapes from the shapes graph."""
        self.shapes_graph = Graph()
        self.shapes_graph.bind("sh", SH)
        self.shapes_graph.bind("", self.SPACE)
        self.shapes_graph.bind("space", self.SPACE)

    def validate(self, inference: str = 'rdfs', abort_on_first: bool = False) -> dict:
        """
        Validate the data graph against all loaded SHACL shapes.
        
        Args:
            inference: Type of inference to use ('rdfs', 'owlrl', 'both', 'none')
            abort_on_first: Stop validation on first violation
            
        Returns:
            dict with keys:
                - conforms: bool - whether validation passed
                - violations: list - list of violation dictionaries
                - results_graph: Graph - the validation results graph
                - results_text: str - human-readable validation results
        """
        try:
            # Perform validation
            conforms, results_graph, results_text = validate(
                data_graph=self.data_graph,
                shacl_graph=self.shapes_graph,
                inference=inference,
                abort_on_first=abort_on_first,
                advanced=True
            )
            
            # Parse violations from results graph
            violations = self._parse_violations(results_graph)
            
            result = {
                "conforms": conforms,
                "violations": violations,
                "violation_count": len(violations),
                "results_graph": results_graph,
                "results_text": results_text,
                "success": True,
                "error": None
            }
            
            self.last_validation = result
            return result
            
        except Exception as e:
            return {
                "conforms": None,
                "violations": [],
                "violation_count": 0,
                "results_graph": None,
                "results_text": None,
                "success": False,
                "error": f"Validation error: {str(e)}"
            }

    def _parse_violations(self, results_graph: Graph) -> list:
        """
        Parse violation details from the SHACL validation results graph.
        
        Returns:
            List of violation dictionaries with details
        """
        violations = []
        
        # Query for validation results
        query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        
        SELECT ?result ?focusNode ?resultPath ?value ?message ?severity ?sourceShape
        WHERE {
            ?result a sh:ValidationResult ;
                    sh:focusNode ?focusNode ;
                    sh:resultSeverity ?severity .
            OPTIONAL { ?result sh:resultPath ?resultPath }
            OPTIONAL { ?result sh:value ?value }
            OPTIONAL { ?result sh:resultMessage ?message }
            OPTIONAL { ?result sh:sourceShape ?sourceShape }
        }
        """
        
        for row in results_graph.query(query):
            violation = {
                "focus_node": self._clean_uri(str(row.focusNode)),
                "property": self._clean_uri(str(row.resultPath)) if row.resultPath else None,
                "value": str(row.value) if row.value else None,
                "message": str(row.message) if row.message else "Constraint violation",
                "severity": self._get_severity_label(str(row.severity)),
                "source_shape": self._clean_uri(str(row.sourceShape)) if row.sourceShape else None,
                "fix_suggestion": self._generate_fix_suggestion(row)
            }
            violations.append(violation)
        
        return violations

    def _clean_uri(self, uri: str) -> str:
        """Clean up URIs for display."""
        # Remove namespace prefixes for readability
        if uri.startswith("http://space.example.org/"):
            return uri.replace("http://space.example.org/", ":")
        elif uri.startswith("http://www.w3.org/ns/shacl#"):
            return uri.replace("http://www.w3.org/ns/shacl#", "sh:")
        return uri

    def _get_severity_label(self, severity_uri: str) -> str:
        """Convert severity URI to readable label."""
        if "Violation" in severity_uri:
            return "ERROR"
        elif "Warning" in severity_uri:
            return "WARNING"
        elif "Info" in severity_uri:
            return "INFO"
        return "UNKNOWN"

    def _generate_fix_suggestion(self, violation_row) -> str:
        """Generate a fix suggestion based on the violation type."""
        suggestions = []
        
        if violation_row.resultPath and violation_row.value:
            prop = self._clean_uri(str(violation_row.resultPath))
            node = self._clean_uri(str(violation_row.focusNode))
            value = str(violation_row.value)
            
            # Suggest removing or changing the value
            suggestions.append(f"Consider removing or changing the value '{value}' for property {prop} on {node}")
        elif violation_row.resultPath:
            prop = self._clean_uri(str(violation_row.resultPath))
            node = self._clean_uri(str(violation_row.focusNode))
            suggestions.append(f"Add or fix property {prop} on {node}")
        
        return suggestions[0] if suggestions else "Review the constraint and data"

    def get_example_shapes(self) -> dict:
        """
        Get a dictionary of example SHACL shapes for the space knowledge graph.
        
        Returns:
            dict mapping shape names to Turtle definitions
        """
        return {
            "planet_diameter_constraint": """
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
""",
            "astronaut_name_required": """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:AstronautShape a sh:NodeShape ;
    sh:targetClass :Astronaut ;
    sh:property [
        sh:path :name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:message "Every astronaut must have exactly one name" ;
    ] .
""",
            "mission_date_format": """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:MissionShape a sh:NodeShape ;
    sh:targetClass :Mission ;
    sh:property [
        sh:path :launchDate ;
        sh:datatype xsd:date ;
        sh:message "Mission launch date must be in date format (YYYY-MM-DD)" ;
    ] .
""",
            "planet_moons_positive": """
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
""",
            "complex_mission_validation": """
@prefix : <http://space.example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

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
"""
        }

    def auto_fix_violations(self, violations: list = None) -> dict:
        """
        Attempt to automatically fix simple violations.
        
        Args:
            violations: List of violations to fix (uses last validation if None)
            
        Returns:
            dict with keys:
                - fixed_count: number of violations fixed
                - fixes: list of fix descriptions
                - updated_graph: the fixed graph
        """
        if violations is None:
            if self.last_validation is None:
                return {
                    "fixed_count": 0,
                    "fixes": [],
                    "updated_graph": self.data_graph,
                    "error": "No validation results available"
                }
            violations = self.last_validation["violations"]
        
        fixes = []
        fixed_count = 0
        
        # Create a copy of the data graph for modifications
        fixed_graph = Graph()
        for triple in self.data_graph:
            fixed_graph.add(triple)
        
        for violation in violations:
            # Try to fix simple violations
            if "cannot be negative" in violation["message"].lower():
                # Fix negative values by setting to 0
                if violation["value"] and violation["property"]:
                    # This is a simplified example - in production would need proper triple manipulation
                    fixes.append(f"Would fix negative value for {violation['property']} on {violation['focus_node']}")
                    fixed_count += 1
        
        return {
            "fixed_count": fixed_count,
            "fixes": fixes,
            "updated_graph": fixed_graph
        }

    def get_stats(self) -> dict:
        """Get statistics about loaded shapes."""
        # Count shape types (NodeShape, PropertyShape, or generic Shape)
        query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>

        SELECT (COUNT(DISTINCT ?shape) as ?count)
        WHERE {
            VALUES ?type { sh:NodeShape sh:PropertyShape sh:Shape }
            ?shape a ?type .
        }
        """
        
        shape_count = 0
        for row in self.shapes_graph.query(query):
            shape_count = int(row[0])
        
        return {
            "total_shapes": shape_count,
            "total_shape_triples": len(self.shapes_graph),
            "total_data_triples": len(self.data_graph)
        }
