from http.server import HTTPServer, BaseHTTPRequestHandler
from server_controller.templating import create_page
from model.game_generator import generate_catan_game


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        get_handlers = {
            "/": self.get_root,
            "/room": self.get_room,
            "/client.js": self.get_room_js,
            "/svg_styles.css": self.get_css,
            "/svg_view.js": self.get_js
        }
        get_handlers[self.path]()

    def do_POST(self):
        pass

    def do_HEAD(self):
        self.protocol_version = "HTTP/1.1"
        head_handlers = {
            "/": lambda: self.send_head("text/html"),
            "/svg_styles.css": lambda: self.send_head("text/css"),
            "/svg_view.js": lambda: self.send_head("text/javascript")
        }
        head_handlers[self.path]()

    def send_head(self, mime_type):
        self.send_response(200)
        self.send_header("Content-type", mime_type)
        self.end_headers()

    def send_resource(self, data, mime_type):
        self.send_response(200)
        self.send_header("Content-type", mime_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def get_root(self):
        game = generate_catan_game()
        page = create_page(game.tiles.values()).encode("utf-8")
        self.send_resource(page, "text/html")

    def get_css(self):
        with open("server_controller/resources/svg_styles.css", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/css")

    def get_js(self):
        with open("server_controller/resources/svg_view.js", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/javascript")

    def get_room(self):
        with open("server_controller/resources/index.html", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/html")

    def get_room_js(self):
        with open("server_controller/resources/client.js", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/javascript")


def start_server():
    host = "127.0.0.1"
    port = 8080
    try:
        print("Serving at {}:{}".format(host, port))
        with HTTPServer((host, port), MyHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nServer closed.")
