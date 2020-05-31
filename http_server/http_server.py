from http.server import HTTPServer, BaseHTTPRequestHandler
from http_server.templating import create_page
from model.game_generator import generate_catan_game


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        get_handlers = {
            "/": self.get_root,
            "/room": self.get_room,
            "/client.js": self.get_room_js,
            "/svg_styles.css": self.get_css,
            "/landing_page_styles.css": self.get_landing_css,
            "/waiting_room_styles.css": self.get_waiting_css,
            "/landing_page_scripts.js": self.get_landing_js,
        }
        get_handlers.get(self.path, self.not_found)()

    def do_POST(self):
        pass

    def do_HEAD(self):
        self.protocol_version = "HTTP/1.1"
        head_handlers = {
            "/": lambda: self.send_head("text/html"),
            "/room": lambda: self.send_head("text/html"),
            "/client.js": lambda: self.send_head("text/javascript"),
            "/svg_styles.css": lambda: self.send_head("text/css")
        }
        head_handlers.get(self.path, self.not_found)()

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

    def not_found(self):
        self.send_error(404)

    def get_root(self):
        player_data = [{"pid": 1, "name": "a", "color": "red"},
                       {"pid": 2, "name": "b", "color": "green"},
                       {"pid": 3, "name": "c", "color": "blue"},
                       {"pid": 4, "name": "d", "color": "yellow"}]
        game = generate_catan_game(player_data)
        page = create_page(game).encode("utf-8")
        self.send_resource(page, "text/html")

    def get_css(self):
        with open("http_server/resources/svg_styles.css", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/css")

    def get_room(self):
        page = create_page().encode("utf-8")
        self.send_resource(page, "text/html")

    def get_room_js(self):
        with open("http_server/resources/client.js", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/javascript")

    def get_landing_css(self):
        with open("http_server/new_frontend/landing_page_styles.css", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/css")

    def get_waiting_css(self):
        with open("http_server/new_frontend/waiting_room_styles.css", "r") as f:
            data = f.read().encode("utf-8")
        self.send_resource(data, "text/css")

    def get_landing_js(self):
        with open("http_server/new_frontend/landing_page_scripts.js", "r") as f:
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
