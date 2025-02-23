"""
Provides input validation and schema enforcement for route optimization data.

This module uses jsonschema to validate that incoming data adheres to the expected schema.
The schema can be extended to include additional fields as required.

Assumptions:
- Data is provided as a dictionary with required fields such as 'route' and 'vehicle_capacity'.
- Additional properties are not allowed.
"""

import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, Any

def validate_route_data(route_data: Dict[str, Any]) -> bool:
    """
    Validate the input route data against the predefined schema.
    
    Args:
        route_data (Dict[str, Any]): Input data containing route and related parameters.
    
    Returns:
        bool: True if validation passes; raises ValidationError if not.
    """
    schema = {
        "type": "object",
        "properties": {
            "route": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 2
            },
            "vehicle_capacity": {"type": "number"},
            "delivery_windows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string", "format": "date-time"},
                        "end": {"type": "string", "format": "date-time"}
                    },
                    "required": ["start", "end"]
                }
            }
        },
        "required": ["route", "vehicle_capacity"],
        "additionalProperties": False
    }
    validate(instance=route_data, schema=schema)
    return True

# Example usage:
if __name__ == "__main__":
    sample_data = {
        "route": [1, 3, 5, 7],
        "vehicle_capacity": 50,
        "delivery_windows": [
            {"start": "2025-01-01T08:00:00Z", "end": "2025-01-01T12:00:00Z"},
            {"start": "2025-01-01T13:00:00Z", "end": "2025-01-01T17:00:00Z"}
        ]
    }
    try:
        if validate_route_data(sample_data):
            print("Route data is valid.")
    except ValidationError as ve:
        print("Validation Error:", ve)
