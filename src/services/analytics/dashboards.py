"""
REST endpoints for BI dashboards and real-time KPI visualization.

This module uses FastAPI to expose endpoints that provide real-time insights into fleet performance.
Endpoints include summaries and detailed metrics. For demonstration, static data is returned.

Assumptions:
- Data is typically fetched from internal databases or data warehouses.
- In production, these endpoints will integrate with our data pipelines.
"""

from fastapi import APIRouter, FastAPI
from typing import Dict, Any

router = APIRouter()

@router.get("/dashboard/summary", response_model=Dict[str, Any])
async def dashboard_summary() -> Dict[str, Any]:
    """
    Get a summary of key performance indicators for fleet optimization.
    
    Returns:
        Dict[str, Any]: A dictionary containing KPI data.
    """
    kpi_data = {
        "on_time_rate": 96.5,
        "average_fuel_consumption": 7.8,  # e.g., liters per 100km
        "total_routes": 120,
        "route_efficiency_improvement": "12%"
    }
    return kpi_data

@router.get("/dashboard/details", response_model=Dict[str, Any])
async def dashboard_details() -> Dict[str, Any]:
    """
    Get detailed dashboard data including historical trends and performance metrics.
    
    Returns:
        Dict[str, Any]: Detailed performance metrics and historical trends.
    """
    details = {
        "historical_on_time_rate": [95, 96, 97, 96.5, 98],
        "fuel_consumption_trends": [8.0, 7.9, 7.7, 7.8, 7.6],
        "route_performance": {
            "Route1": {"distance": 150, "time": 180, "efficiency": "90%"},
            "Route2": {"distance": 200, "time": 240, "efficiency": "92%"}
        }
    }
    return details

# Create FastAPI app for standalone testing.
app = FastAPI()
app.include_router(router, prefix="/api")

# To run the server: uvicorn dashboards:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboards:app", host="0.0.0.0", port=8000, reload=True)
