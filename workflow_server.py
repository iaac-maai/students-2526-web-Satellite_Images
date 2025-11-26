import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# >>>>>>>>>>>>>>>>> CONFIG - EDIT THESE <<<<<<<<<<<<<<<<<
OWNER = "RashiD2801"     
REPO = "SATELLITE_IMAGES"                    # e.g. "satellite-mapbox"
WORKFLOW_FILE = "fetch_map_image.yml"   # exact file name in .github/workflows/
GIT_REF = "main"                           # branch name, often "main" or "master"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

GITHUB_API_URL = (
    f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
)

PAT = os.environ.get("GITHUB_WORKFLOW_PAT")
if not PAT:
    raise SystemExit(
        "ERROR: GITHUB_WORKFLOW_PAT environment variable not set.\n"
        "Set it to your GitHub personal access token and run again."
    )

app = Flask(__name__)
CORS(app)  # allow requests from your map page

@app.route("/run-workflow", methods=["POST"])
def run_workflow():
    data = request.get_json() or {}
    lat = data.get("lat")
    lon = data.get("lon")

    if not lat or not lon:
        return jsonify({"error": "lat and lon are required"}), 400

    # Build the payload for GitHub workflow_dispatch
    payload = {
        "ref": GIT_REF,
        "inputs": {
            "lat": str(lat),
            "lon": str(lon),
        },
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {PAT}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        resp = requests.post(GITHUB_API_URL, json=payload, headers=headers, timeout=20)
    except Exception as e:
        return jsonify({"error": f"Request to GitHub failed: {e}"}), 500

    # GitHub returns 204 No Content on success
    if resp.status_code == 204:
        return jsonify(
            {
                "status": "ok",
                "message": "Workflow dispatched. Check your GitHub Actions tab.",
            }
        ), 200
    else:
        return jsonify(
            {
                "status": "error",
                "github_status": resp.status_code,
                "github_response": resp.text,
            }
        ), 500


if __name__ == "__main__":
    # Run on localhost:8000
    app.run(host="127.0.0.1", port=8000, debug=True)
    