import sys
import json
import logging
import requests
from splunklib.binding import connect
from splunklib.client import Service

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("RunSavedSearch")

def run_saved_search(settings):
    try:
        # Load alert action parameters
        results_file = settings.get("results_file")
        with open(results_file, "r") as f:
            results = json.load(f)

        # Retrieve parameters from alert action
        saved_search_name = settings.get("configuration").get("saved_search_name")
        splunk_url = settings.get("server_uri")
        session_key = settings.get("session_key")

        # Connect to Splunk REST API
        headers = {"Authorization": f"Bearer {session_key}"}
        url = f"{splunk_url}/services/saved/searches/{saved_search_name}/dispatch"
        response = requests.post(url, headers=headers, verify=False)

        if response.status_code == 201:
            logger.info(f"Successfully triggered saved search: {saved_search_name}")
        else:
            logger.error(f"Failed to trigger saved search: {response.text}")

    except Exception as e:
        logger.error(f"Error running saved search: {str(e)}")

if __name__ == "__main__":
    run_saved_search(json.loads(sys.stdin.read()))
