# splunk_itsi_mcp_server.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
import requests
import urllib3
import json
from collections import Counter

# --- Print a version identifier to the logs ---
print("--- Running Script Version: SPLUNK_ITSI_V5_ADVANCED ---", file=sys.stderr)

# --- Find and Load the .env File ---
script_location = Path(__file__).resolve().parent
env_file_path = script_location / '.env'
load_dotenv(dotenv_path=env_file_path)

# --- Load Credentials ---
SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")

# --- Disable SSL Warnings ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Splunk ITSI API Connector Class ---
class SplunkITSI_APIConnector:
    """Handles direct API communication with the Splunk ITSI and Core Splunk platforms."""
    def __init__(self, base_url, username, password):
        if not all([base_url, username, password]):
            raise ValueError("Missing Splunk credentials. Please provide SPLUNK_URL, SPLUNK_USERNAME, and SPLUNK_PASSWORD in .env file.")

        self.base_url = f"{base_url.rstrip('/')}:8089"
        self.session = requests.Session()
        self.session.verify = False
        self.session.auth = (username, password)
        print("--- Using Username/Password authentication ---", file=sys.stderr)

    def get(self, endpoint, params=None):
        """Performs a GET request to a Splunk API endpoint."""
        url = f"{self.base_url}{endpoint}"
        query_params = {'output_mode': 'json'}
        if params:
            query_params.update(params)
            
        response = self.session.get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        """Performs a POST request to a Splunk API endpoint."""
        url = f"{self.base_url}{endpoint}"
        # Splunk POST requests often use form-encoded data
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()

# --- Create the MCP Server ---
mcp = FastMCP(
    name="Splunk ITSI MCP",
    instructions="An MCP server for Splunk ITSI with end-to-end service visibility and core Splunk access."
)

# --- Helper Function to Initialize the Connector ---
def get_connector():
    """Creates an instance of the SplunkITSI_APIConnector."""
    return SplunkITSI_APIConnector(SPLUNK_URL, SPLUNK_USERNAME, SPLUNK_PASSWORD)

# --- NEW: Core Splunk and Service Analyzer Tools ---
@mcp.tool()
def get_service_analyzer_view() -> dict:
    """Retrieves the high-level service health view from the ITSI Service Analyzer."""
    try:
        connector = get_connector()
        # This endpoint provides the data for the main Service Analyzer page
        return connector.get("/servicesNS/nobody/SA-ITOA/itoa_interface/service_analyzer_view")
    except Exception as e:
        print(f"Error in get_service_analyzer_view tool: {e}", file=sys.stderr)
        return {"error": str(e)}

@mcp.tool()
def run_splunk_search(search_query: str) -> dict:
    """
    Executes a Splunk search query (SPL) and returns the results.
    
    Args:
        search_query: The SPL query to execute (e.g., "search index=_internal | head 10").
    """
    try:
        connector = get_connector()
        # The search/jobs endpoint is used to run searches
        data = {'search': search_query}
        return connector.post("/services/search/jobs/export", data=data)
    except Exception as e:
        print(f"Error in run_splunk_search tool: {e}", file=sys.stderr)
        return {"error": str(e)}

@mcp.tool()
def get_splunk_indexes() -> dict:
    """Retrieves a list of all configured indexes in Splunk."""
    try:
        connector = get_connector()
        return connector.get("/services/data/indexes")
    except Exception as e:
        print(f"Error in get_splunk_indexes tool: {e}", file=sys.stderr)
        return {"error": str(e)}

# --- Existing Visualization Tool ---
@mcp.tool()
def visualize_service_health() -> str:
    """Generates an HTML bar chart visualizing the health scores of all ITSI services."""
    try:
        connector = get_connector()
        services = connector.get("/servicesNS/nobody/SA-ITOA/itoa_interface/service")
        
        health_data = []
        for service in services:
            health_data.append({
                "service_title": service.get("title", "N/A"),
                "health_score": service.get("health_score", 0)
            })

        if not health_data:
            return "<html><body><h1>No Data</h1><p>Could not retrieve service health data.</p></body></html>"

        labels = [service['service_title'] for service in health_data]
        data = [service['health_score'] for service in health_data]
        
        background_colors = []
        for score in data:
            if score <= 60: background_colors.append('rgba(255, 99, 132, 0.8)') # Red
            elif score <= 80: background_colors.append('rgba(255, 206, 86, 0.8)') # Yellow
            else: background_colors.append('rgba(75, 192, 192, 0.8)') # Green

        chart_config = {
            "type": 'bar',
            "data": {
                "labels": labels,
                "datasets": [{"label": 'Health Score', "data": data, "backgroundColor": background_colors}]
            },
            "options": {
                "responsive": True, "indexAxis": 'y',
                "scales": {"x": {"beginAtZero": True, "max": 100}},
                "plugins": {"legend": {"display": False}, "title": {"display": True, "text": 'Health Score (0-100)'}}
            }
        }
        chart_config_json = json.dumps(chart_config)

        html_content = f"""
        <!DOCTYPE html><html><head><title>ITSI Service Health</title><script src="https://cdn.jsdelivr.net/npm/chart.js"></script><style>body{{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}.chart-container{{width:90%;max-width:1000px;padding:20px;background:white;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.1);}}h1{{text-align:center;}}</style></head><body><div class="chart-container"><h1>ITSI Service Health Overview</h1><canvas id="healthChart"></canvas></div><script>new Chart(document.getElementById('healthChart').getContext('2d'), {chart_config_json});</script></body></html>
        """
        return html_content
    except Exception as e:
        print(f"Error in visualize_service_health tool: {e}", file=sys.stderr)
        return f"<html><body><h1>Error</h1><p>Could not generate visualization: {e}</p></body></html>"

# --- Main Execution Block ---
if __name__ == "__main__":
    mcp.run()
