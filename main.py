import asyncio

from websocketPool import client
from websocketPool import client_pool

if __name__ == "__main__":
    uris = {
        "a": "ws://127.0.0.1:12345",
        "b": "ws://127.0.0.1:12346",
    }
    def on_recv_msg(name, msg):
        print(f"Client {name} received: {msg}")

    cp = client_pool.ClientPool(
        "cp1", {{name: client.Client(uri=uri,recvMsgFn=on_recv_msg).connect()} for name, uri in uris.items()}
    )
    
    asyncio.run(cp.run())

    asyncio.get_event_loop().run_until_complete(client.connect())
