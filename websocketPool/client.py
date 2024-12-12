import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, server!")
        response = await websocket.recv()
        print(f"Received from server: {response}")
        
        
def main():
    hello()
    
if __name__ == "__main__":
    main()