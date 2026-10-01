# api.py - serves the latest Pulse reading over HTTP
import json, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

def latest_reading():
    conn = sqlite3.connect("pulse.db")
    row = conn.execute("SELECT timestamp, uptime_s, mem_available_kb, cpu_temp_c FROM readings ORDER BY timestamp DESC LIMIT 1;").fetchone()
    conn.close()
    if row is None:
        return None
    return{
        "timestamp": row[0],
        "uptime_s": row[1],
        "mem_available_kb": row[2],
        "cpu_temp_c": row[3],
    }

class PulseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            body = json.dumps(latest_reading()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("localhost", 8000), PulseHandler)
print("Pulse API running at http://localhost:8000/status")
server.serve_forever()