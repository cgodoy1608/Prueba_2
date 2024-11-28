from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "127.0.0.1"
PORT = 8080

devices = []
file_name = "devices.json"

# Load devices from a file
def load_devices():
    try:
        with open(file_name, "r") as file:
            global devices
            devices = json.load(file)
    except FileNotFoundError:
        devices = []

# Save devices to a file
def save_devices():
    with open(file_name, "w") as file:
        json.dump(devices, file)

class DeviceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/devices":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(devices).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint no encontrado.")

    def do_POST(self):
        if self.path == "/devices":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            try:
                device = json.loads(post_data)
                devices.append(device)
                save_devices()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Dispositivo añadido con éxito"}).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error en el formato del JSON.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint no encontrado.")

    def do_DELETE(self):
        if self.path.startswith("/devices/"):
            ip_address = self.path.split("/")[-1]
            global devices
            devices = [d for d in devices if d["ip_address"] != ip_address]
            save_devices()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"Dispositivo con IP {ip_address} eliminado."}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint no encontrado.")

def run():
    load_devices()
    server = HTTPServer((HOST, PORT), DeviceHandler)
    print(f"Servidor corriendo en http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()
