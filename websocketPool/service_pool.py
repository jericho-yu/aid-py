import asyncio
import websockets

class WebSocketPool:
    def __init__(self, max_connections):
        self.max_connections = max_connections
        self.connections = asyncio.Queue()

    async def get_connection(self):
        if self.connections.empty():
            await self.create_connection()
        return await self.connections.get()

    async def return_connection(self, connection):
        await self.connections.put(connection)

    async def create_connection(self):
        # 创建一个新的 WebSocket 连接
        connection = await websockets.connect('ws://localhost:8765')
        await self.connections.put(connection)

    async def close_all(self):
        while not self.connections.empty():
            connection = await self.connections.get()
            await connection.close()

async def handle_connection(websocket, path):
    pool = WebSocketPool(10)  # 最大10个连接
    connection = await pool.get_connection()
    try:
        # 使用连接进行通信
        while True:
            data = await websocket.recv()
            await connection.send(data)
    except websockets.ConnectionClosed:
        pass
    finally:
        await pool.return_connection(connection)

start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()