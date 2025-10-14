from http.server import BaseHTTPRequestHandler, HTTPServer
import json


data = []

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header("content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        content_size = int(self.headers.get("content-Length", 0))
        parsed_data = self.rfile.read(content_size)

        post_data = json.loads(parsed_data)
        print(post_data)
        data.append(post_data)
        self.send_data(
            [
            {"Message": "Data Received"},
            {"data": post_data}
        ], status = 200)


def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("Starting server on port 8000....")
    httpd.serve_forever()

print("Running server ")
run()



