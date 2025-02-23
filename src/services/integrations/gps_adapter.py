"""
Adapts external GPS data into our system.

This module simulates integration with external GPS data providers.
It contains functions to retrieve and format GPS data from external APIs, which
can then be processed by our data ingestion pipeline.

Assumptions:
- External GPS APIs return data in JSON format.
- In a production system, proper authentication and error handling must be implemented.
"""

import requests
import logging

# Configure logger.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_gps_data(device_id: str) -> dict:
    """
    Fetch GPS data for a given device from an external API.

    Args:
        device_id (str): Unique identifier for the GPS device.

    Returns:
        dict: GPS data including latitude, longitude, and timestamp.
    """
    # In a real implementation, replace the URL with the actual GPS data API endpoint.
    api_url = f"https://api.example.com/gps/{device_id}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        gps_data = response.json()
        logger.info(f"Fetched GPS data for device {device_id}")
        return gps_data
    except requests.RequestException as e:
        logger.error(f"Error fetching GPS data for device {device_id}: {e}")
        # Fallback: return simulated GPS data.
        return {"device_id": device_id, "latitude": 0.0, "longitude": 0.0, "timestamp": "1970-01-01T00:00:00Z"}

# Example usage:
if __name__ == "__main__":
    device_id = "GPS12345"
    data = fetch_gps_data(device_id)
    print("GPS Data:", data)
