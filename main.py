import asyncio
from websocketPool.service_pool import WebsocketPool


if __name__ == "__main__":
    websocket_pool = WebsocketPool()
    asyncio.run(websocket_pool.serve())
