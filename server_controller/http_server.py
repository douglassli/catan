from http.server import HTTPServer, BaseHTTPRequestHandler
from server_controller.templating import create_page
from model.game_generator import generate_catan_game


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        if self.path == "/":
            data = self.get_root()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/svg_styles.css":
            data = self.get_css()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    def do_HEAD(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        if self.path == "/":
            self.send_header("Content-type", "text/html")
        elif self.path == "/svg_styles.css":
            self.send_header("Content-type", "text/css")
        self.end_headers()

    def get_root(self):
        data = generate_catan_game().as_data()
        page = create_page(data).encode("utf-8")
        return page

    def get_css(self):
        with open("server_controller/resources/svg_styles.css", "r") as f:
            return f.read().encode("utf-8")


def start_server():
    with HTTPServer(("127.0.0.1", 8080), MyHTTPRequestHandler) as httpd:
        httpd.serve_forever()
