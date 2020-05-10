from server_controller.catan_server import CatanServer
from server_controller.http_server import start_server
import websockets
import asyncio


def main():
    server = CatanServer()
    start_server = websockets.serve(server.consumer_handler, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    start_server()
