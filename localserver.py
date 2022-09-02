from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import blockerwebsite


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        data = blockerwebsite.read_file()
        self.wfile.write(json.dumps(data).encode('utf-8'))



def start():
    PORT = 9000
    server = HTTPServer(('', PORT), Handler)
    print('Server running on port ' + str(PORT))
    server.serve_forever()