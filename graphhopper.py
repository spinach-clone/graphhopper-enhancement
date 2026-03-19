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

# BUG FIX: Warn early if API key is missing instead of getting a cryptic error later
if not api_key:
    print("[ERROR] API_KEY not found in .env file. Please check your .env setup.")

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Dark or Light mode */
        :root {
            --bg: #9c8dec;
            --card-bg: #fafafa;
            --text: #333;
            --subtext: #6c757d;
            --input-bg: #f4f2f3;
            --input-border: #ccc;
            --output-bg: #eee;
            --hr-color: #ddd;
        }

        body.dark {
            --bg: #1e1b2e;
            --card-bg: #2a2640;
            --text: #e0e0e0;
            --subtext: #aaa;
            --input-bg: #3a3550;
            --input-border: #555;
            --output-bg: #1a1828;
            --hr-color: #444;
        }

        body {
            height: 90vh;
            font-family: sans-serif;
            padding: 20px;
            background: var(--bg);
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background 0.3s;
        }

        .container {
            max-width: 500px;
            width: 100%;
            margin: auto;
            background: var(--card-bg);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            color: var(--text);
            transition: background 0.3s, color 0.3s;
        }

        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid var(--input-border);
            border-radius: 4px;
            box-sizing: border-box;
            background: var(--input-bg);
            color: var(--text);
            transition: background 0.3s, color 0.3s;
        }

        input:focus {
            border: 2px solid #9c8dec;
            outline: none;
        }

        button {
            background: #9c8dec;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
        }

        button:hover { background: #c9c1f0; }

        #output {
            margin-top: 20px;
            white-space: pre-wrap;
            font-size: 0.9em;
            background: var(--output-bg);
            color: var(--text);
            padding: 10px;
            border-radius: 4px;
            max-height: 300px;
            overflow-y: auto;
            transition: background 0.3s, color 0.3s;
        }

        .instruction {
            border-bottom: 1px solid var(--hr-color);
            padding: 5px 0;
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }

        /* Dark mode toggle switch */
        .toggle-label {
            font-size: 0.8em;
            color: var(--subtext);
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }

        .toggle-switch {
            position: relative;
            width: 36px;
            height: 20px;
        }

        .toggle-switch input { display: none; }

        .slider {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #ccc;
            border-radius: 20px;
            transition: 0.3s;
        }

        .slider:before {
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
            left: 3px;
            bottom: 3px;
            background: white;
            border-radius: 50%;
            transition: 0.3s;
        }

        input:checked + .slider { background: #9c8dec; }
        input:checked + .slider:before { transform: translateX(16px); }

        .error-msg { color: #e55; font-weight: bold; }
        .step-num { color: #9c8dec; font-weight: bold; margin-right: 5px; }
        /* FEATURE: Color-coded turn instructions - Roamar */
        .step-turn-left  { border-left: 4px solid #f0ad4e; padding-left: 6px; }
        .step-turn-right { border-left: 4px solid #5bc0de; padding-left: 6px; }
        .step-arrive     { border-left: 4px solid #5cb85c; padding-left: 6px; font-weight: bold; }
        .step-continue   { border-left: 4px solid #aaa;    padding-left: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="top-bar">
            <h2 style="margin: 0; color: #9c8dec;">PRECISE</h2>
            <!-- INNOVATION: Dark/Light mode toggle -->
            <label class="toggle-label">
                🌗 Toggle Preference
                <div class="toggle-switch">
                    <input type="checkbox" id="darkToggle" onchange="toggleDark()">
                    <span class="slider"></span>
                </div>
            </label>
        </div>

        <p style="text-align: center; color: var(--subtext); margin-top: -5px;">
            A Text-based direction system for accurate navigation
        </p>

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
        // INNOVATION: Dark mode toggle
        function toggleDark() {
            document.body.classList.toggle('dark');
        }

        async function calculateRoute() {
            const vehicle = document.getElementById('vehicle').value;
            const start = document.getElementById('start').value.trim();
            const dest = document.getElementById('dest').value.trim();
            const output = document.getElementById('output');

            // BUG FIX: Input validation before hitting the API
            if (!start || !dest) {
                output.innerHTML = "<span class='error-msg'>⚠️ Please enter both a starting location and a destination.</span>";
                return;
            }

            if (start.toLowerCase() === dest.toLowerCase()) {
                output.innerHTML = "<span class='error-msg'>⚠️ Start and destination cannot be the same.</span>";
                return;
            }

            output.innerHTML = "⏳ Loading directions...";

            const result = await pywebview.api.get_route(start, dest, vehicle);

            if (result.error) {
                output.innerHTML = "<span class='error-msg'>❌ Error: " + result.error + "</span>";
            } else {
                let html = `<b>📍 ${result.origin} → ${result.destination}</b><br>`;
                html += `🛣️ Distance: ${result.km} km / ${result.miles} miles<br>`;
                html += `⏱️ Duration: ${result.time}<br><hr>`;

                // INNOVATION: Numbered steps for easier reading
                // FEATURE: Color-coded turn instructions - Roamar
                result.instructions.forEach((step, index) => {
                    let colorClass = "step-continue";
                    const s = step.toLowerCase();
                    if (s.includes("arrive"))               colorClass = "step-arrive";
                    else if (s.includes("left"))            colorClass = "step-turn-left";
                    else if (s.includes("right"))           colorClass = "step-turn-right";
                    html += `<div class="instruction ${colorClass}"><span class="step-num">${index + 1}.</span>${step}</div>`;
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
        # BUG FIX: Guard against missing API key
        if not api_key:
            return None

        url = self.geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": api_key})

        try:
            response = requests.get(url, timeout=10)  # BUG FIX: Added timeout to prevent hanging
            data = response.json()

            if response.status_code == 200 and data.get("hits"):
                hit = data["hits"][0]
                return {
                    "lat": hit["point"]["lat"],
                    "lng": hit["point"]["lng"],
                    "name": hit.get("name", location)
                }
        except requests.exceptions.Timeout:
            print(f"[ERROR] Geocode request timed out for: {location}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Geocode request failed: {e}")

        return None

    def get_route(self, start_loc, dest_loc, vehicle):
        try:
            # BUG FIX: Check API key early and return friendly error
            if not api_key:
                return {"error": "API key is missing. Please check your .env file."}

            # 1. Geocode Start
            origin = self._get_geocode(start_loc)
            # 2. Geocode Destination
            dest = self._get_geocode(dest_loc)

            if not origin:
                return {"error": f"Could not find starting location: '{start_loc}'"}
            if not dest:
                return {"error": f"Could not find destination: '{dest_loc}'"}

            # 3. Get Route
            params = {
                "key": api_key,
                "vehicle": vehicle,
                "point": [f"{origin['lat']},{origin['lng']}", f"{dest['lat']},{dest['lng']}"]
            }

            route_res = requests.get(self.route_url, params=params, timeout=10)  # BUG FIX: Added timeout
            route_data = route_res.json()

            if route_res.status_code != 200:
                return {"error": route_data.get("message", "Routing failed. Check your API key or locations.")}

            path = route_data["paths"][0]
            dist_km = path["distance"] / 1000

            # Format time
            total_ms = path["time"]
            seconds = int((total_ms / 1000) % 60)
            minutes = int((total_ms / (1000 * 60)) % 60)
            hours = int((total_ms / (1000 * 60 * 60)))

            instructions = [
                f"{i['text']} ({i['distance'] / 1000:.1f} km)"
                for i in path["instructions"]
            ]

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
    window = webview.create_window(
        'PRECISE: An Enhanced Map Navigation System with Graphhopper',
        html=HTML_INTERFACE,
        js_api=bridge
    )
    webview.start()