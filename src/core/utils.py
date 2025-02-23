"""
Contains common helper functions used across the fleet optimization platform.

Functions include:
- calculate_distance: Compute distance between two points (using Haversine formula).
- format_date: Standardize date/time formatting.
- validate_numeric: Check if input is numeric and within an expected range.
- merge_dicts: Merge two dictionaries recursively.
"""

import math
from datetime import datetime
from typing import Any, Dict

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth surface using the Haversine formula.
    
    Args:
        lat1 (float): Latitude of point 1.
        lon1 (float): Longitude of point 1.
        lat2 (float): Latitude of point 2.
        lon2 (float): Longitude of point 2.
        
    Returns:
        float: Distance in kilometers.
    """
    # Convert degrees to radians.
    rlat1, rlon1 = math.radians(lat1), math.radians(lon1)
    rlat2, rlon2 = math.radians(lat2), math.radians(lon2)
    
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    
    a = math.sin(dlat/2)**2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    earth_radius = 6371  # in kilometers
    return earth_radius * c

def format_date(date_obj: datetime, format_str: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    """
    Format a datetime object into a string using the given format.
    
    Args:
        date_obj (datetime): The datetime object to format.
        format_str (str): The format string.
        
    Returns:
        str: Formatted date string.
    """
    return date_obj.strftime(format_str)

def validate_numeric(value: Any, min_value: float = None, max_value: float = None) -> bool:
    """
    Validate that the provided value is numeric and within the specified range.
    
    Args:
        value (Any): The value to check.
        min_value (float, optional): Minimum allowed value.
        max_value (float, optional): Maximum allowed value.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return False
    
    if min_value is not None and num < min_value:
        return False
    if max_value is not None and num > max_value:
        return False
    return True

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Recursively merge two dictionaries.
    
    Args:
        dict1 (Dict): Base dictionary.
        dict2 (Dict): Dictionary with values to merge.
        
    Returns:
        Dict: Merged dictionary.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

# Example usage:
if __name__ == "__main__":
    # Calculate distance between two cities (e.g., New York and London).
    ny_lat, ny_lon = 40.7128, -74.0060
    london_lat, london_lon = 51.5074, -0.1278
    distance = calculate_distance(ny_lat, ny_lon, london_lat, london_lon)
    print(f"Distance from New York to London: {distance:.2f} km")
    
    # Format current date.
    now = datetime.utcnow()
    print("Formatted date:", format_date(now))
    
    # Validate a numeric value.
    print("Is 50 valid between 0 and 100?", validate_numeric(50, 0, 100))
    
    # Merge two dictionaries.
    dict_a = {"a": 1, "b": {"x": 10}}
    dict_b = {"b": {"y": 20}, "c": 3}
    merged = merge_dicts(dict_a, dict_b)
    print("Merged Dictionary:", merged)
