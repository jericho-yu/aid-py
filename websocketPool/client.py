import asyncio
from typing import Callable, Union
import websockets


class Client:
    def __init__(
        self, uri: str, recvMsgFn: Callable[[str, Union[str, bytes]], None] = None
    ) -> None:
        self.uri = uri
        self.websocket = None
        self.name = ""
        self.recvMsgFn = recvMsgFn

    async def connect(self) -> "Client":
        """
        执行链接
        :returns:Client
        """
        self.websocket = await websockets.connect(self.uri)
        return self

    async def set_name(self, name: str) -> "Client":
        """
        设置名称
        :returns:Client
        """
        self.name = name
        return self

    async def get_name(self) -> str:
        """
        读取名称
        :returns self.name:str
        """
        return self.name

    async def send(self, message) -> "Client":
        """
        发送消息
        :param message:str 消息
        :returns:Client
        """
        await self.websocket.send(message)
        return self

    async def recv(self):
        """
        接收消息
        """
        while True:
            receiver = await self.websocket.recv()
            print(f"Client {self.name} received: {receiver}")
            if self.recvMsgFn:
                await self.recvMsgFn(self.name, receiver)

    async def close(self) -> "Client":
        """
        关闭连接
        :returns:Client
        """
        await self.websocket.close()

    async def __aenter__(self) -> "Client":
        return await self.connect()

    async def __aexit__(self, exc_type, exc_value, traceback) -> "Client":
        return await self.close()


async def main():
    clients = {
        "a": Client(f"ws://127.0.0.1:12345"),
        "b": Client(f"ws://127.0.0.1:12346"),
    }

    await asyncio.gather(*(client.connect() for client in clients.values()))
    await asyncio.gather(*(client.send(f"hello {i}") for i, client in clients.items()))

    tasks = [asyncio.create_task(client.recv(None)) for client in clients.values()]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    print("beginning")


if __name__ == "__main__":
    asyncio.run(main())
