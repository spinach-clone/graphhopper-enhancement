#Team IntelleX
#Members:
# Diano, Francis Miguel
# Ejares, Allyssa Faith
# Espina, Christo Rey
# Roamar, Kaycee


import webview
import requests
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { height: 90vh; font-family: sans-serif; padding: 20px; background: #9c8dec; display: flex; justify-content: center; align-items: center; }
        .container { max-width: 500px; margin: auto; background: #fafafa; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input, select, button { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; background: #f4f2f3}
        input:focus { border: 2px solid #9c8dec; outline: none; }
        button { background: #9c8dec; color: white; border: none; cursor: pointer; font-weight: bold; border-radius: 5px;}
        button:hover { background: #c9c1f0; }
        #output { margin-top: 20px; white-space: pre-wrap; font-size: 0.9em; background: #eee; padding: 10px; border-radius: 4px; max-height: 300px; overflow-y: auto; }
        .instruction { border-bottom: 1px solid #ddd; padding: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align: center; color: #9c8dec">PRECISE</h2>
        <p style="text-align: center; color: #6c757d; margin-top: -10px;">A Text-based direction system for accurate navigation</p>
        <label>Vehicle Profile:</label>
        <select id="vehicle">
            <option value="car">Car</option>
            <option value="bike">Bike</option>
            <option value="foot">Foot</option>
        </select>
        <input type="text" id="start" placeholder="Starting Location (e.g., Berlin)">
        <input type="text" id="dest" placeholder="Destination (e.g., Munich)">
        <button onclick="calculateRoute()">Get Directions</button>
        <div id="output">Results will appear here...</div>
    </div>

    <script>
        async function calculateRoute() {
            const vehicle = document.getElementById('vehicle').value;
            const start = document.getElementById('start').value;
            const dest = document.getElementById('dest').value;
            const output = document.getElementById('output');

            output.innerHTML = "Loading...";

            // Call the Python function exposed via pywebview
            const result = await pywebview.api.get_route(start, dest, vehicle);

            if (result.error) {
                output.innerHTML = "<span style='color:red'>Error: " + result.error + "</span>";
            } else {
                let html = `<b>Directions from ${result.origin} to ${result.destination}</b><br>`;
                html += `Distance: ${result.km} km / ${result.miles} miles<br>`;
                html += `Duration: ${result.time}<br><hr>`;

                result.instructions.forEach(step => {
                    html += `<div class="instruction">${step}</div>`;
                });
                output.innerHTML = html;
            }
        }
    </script>
</body>
</html>
"""


class ApiBridge:
    def __init__(self):
        self.route_url = "https://graphhopper.com/api/1/route?"
        self.geocode_url = "https://graphhopper.com/api/1/geocode?"

    def _get_geocode(self, location):
        url = self.geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": api_key})
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("hits"):
            hit = data["hits"][0]
            return {
                "lat": hit["point"]["lat"],
                "lng": hit["point"]["lng"],
                "name": hit.get("name", location)
            }
        return None

    def get_route(self, start_loc, dest_loc, vehicle):
        try:
            # 1. Geocode Start
            origin = self._get_geocode(start_loc)
            # 2. Geocode Destination
            dest = self._get_geocode(dest_loc)

            if not origin or not dest:
                return {"error": "Could not find one of the locations."}

            # 3. Get Route
            params = {
                "key": api_key,
                "vehicle": vehicle,
                "point": [f"{origin['lat']},{origin['lng']}", f"{dest['lat']},{dest['lng']}"]
            }
            # Note: requests handles list params as multiple 'point=' keys automatically
            route_res = requests.get(self.route_url, params=params)
            route_data = route_res.json()

            if route_res.status_code != 200:
                return {"error": route_data.get("message", "Routing failed")}

            path = route_data["paths"][0]
            dist_km = path["distance"] / 1000

            # Format time
            total_ms = path["time"]
            seconds = int((total_ms / 1000) % 60)
            minutes = int((total_ms / (1000 * 60)) % 60)
            hours = int((total_ms / (1000 * 60 * 60)))

            instructions = [f"{i['text']} ({i['distance'] / 1000:.1f} km)" for i in path["instructions"]]

            return {
                "origin": origin["name"],
                "destination": dest["name"],
                "km": round(dist_km, 1),
                "miles": round(dist_km / 1.61, 1),
                "time": f"{hours:02d}:{minutes:02d}:{seconds:02d}",
                "instructions": instructions
            }

        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    bridge = ApiBridge()
    window = webview.create_window('PRECISE: An Enhanced Map Navigation System with Graphhopper', html=HTML_INTERFACE, js_api=bridge)
    webview.start()