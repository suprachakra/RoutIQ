"""
Generates detailed reports and analytics for fleet performance.

This module provides functions to generate textual reports based on fleet performance data,
including summary analytics, trend analysis, and KPI breakdowns.

Assumptions:
- Data is supplied as a dictionary from our analytics layer.
- For demonstration, static data is used.
"""

def generate_performance_report(data: dict) -> str:
    """
    Generate a detailed performance report based on provided data.
    
    Args:
        data (dict): A dictionary containing performance metrics.
    
    Returns:
        str: A formatted report string.
    """
    report_lines = []
    report_lines.append("Fleet Performance Report")
    report_lines.append("-------------------------")
    report_lines.append(f"On-Time Rate: {data.get('on_time_rate', 'N/A')}%")
    report_lines.append(f"Average Fuel Consumption: {data.get('average_fuel_consumption', 'N/A')} L/100km")
    report_lines.append(f"Total Routes: {data.get('total_routes', 'N/A')}")
    report_lines.append(f"Route Efficiency Improvement: {data.get('route_efficiency_improvement', 'N/A')}")
    
    if "historical_on_time_rate" in data:
        report_lines.append("\nHistorical On-Time Rates:")
        report_lines.append(", ".join(map(str, data["historical_on_time_rate"])))
    
    if "fuel_consumption_trends" in data:
        report_lines.append("\nFuel Consumption Trends:")
        report_lines.append(", ".join(map(str, data["fuel_consumption_trends"])))
    
    return "\n".join(report_lines)

# Example usage:
if __name__ == "__main__":
    sample_data = {
        "on_time_rate": 96.5,
        "average_fuel_consumption": 7.8,
        "total_routes": 120,
        "route_efficiency_improvement": "12%",
        "historical_on_time_rate": [95, 96, 97, 96.5, 98],
        "fuel_consumption_trends": [8.0, 7.9, 7.7, 7.8, 7.6]
    }
    report = generate_performance_report(sample_data)
    print(report)
