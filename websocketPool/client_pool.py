import asyncio
from typing import Dict, List
from websocketPool.client import Client


class ClientNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ClientPool:
    def __init__(self, name: str, clients: Dict[str, Client]) -> None:
        self.name = name
        self.clients = clients

    async def set_name(self, name: str) -> "ClientPool":
        """
        设置连接池名称
        :param name: str
        :return: ClientPool
        """
        self.name = name
        return self

    async def get_name(self) -> str:
        """
        获取连接池名称
        :return: str
        """
        return self.name

    async def set_clients(self, clients: List[Client]) -> "ClientPool":
        """
        设置客户端连接
        """
        self.clients = clients
        return self

    async def get_clients(self) -> Dict[str, Client]:
        """
        获取客户端连接
        """
        return self.clients

    async def append_client(self, name: str, client: Client) -> "ClientPool":
        """
        添加客户端
        :param name: str 客户端名称
        :param client: Client 客户端
        :return: ClientPool
        """
        if name in self.clients:
            raise ClientNotFound(f"Client {name} already exists")

        self.clients[name] = client
        return self

    async def remove_key(self, name: str) -> "ClientPool":
        """
        移除客户端
        :param name: str 客户端名称
        :return: ClientPool
        """
        if name in self.clients:
            del self.clients[name]
        return self

    async def send_msg(self, name: str, msg: str) -> "ClientPool":
        """
        发送消息
        :param name: str 客户端名称
        :param msg: str 消息
        :return: ClientPool
        """
        if name in self.clients:
            await self.clients[name].send(msg)
        return self

    async def run(self) -> "ClientPool":
        """
        运行
        :return: ClientPool
        """
        if self.clients:
            tasks = [
                asyncio.create_task(client.recv()) for client in self.clients.values()
            ]
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
