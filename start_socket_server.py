from server_controller.catan_server import CatanServer
import websockets
import asyncio


def main():
    server = CatanServer()
    server_start = websockets.serve(server.consumer_handler, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(server_start)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
