from http.server import BaseHTTPRequestHandler, HTTPServer
import json
class BasicAPI(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    def do_DELETE(self):
      
        response = {
            "message": "DELETE request received — item deleted successfully"
        }
        self._set_headers(200)
        self.wfile.write(json.dumps(response).encode('utf-8'))
def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print(" DELETE Server running at http://localhost:8000")
    httpd.serve_forever()
print("Running server")
run()