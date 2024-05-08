from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000


class UploadHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()


    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            with open('recording.mp3', 'wb') as f:
                f.write(post_data)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'audio received')




server = HTTPServer(('localhost', PORT), UploadHandler)

print(f'Servidor rodando em http://localhost:{PORT}/upload')
server.serve_forever()
