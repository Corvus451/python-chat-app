import asyncio
import websockets
from websockets.asyncio.server import serve
import json

clients: set[websockets.ServerConnection] = set()

def parse_message(msg: str) -> dict:
    if not msg:
        return None
    return json.loads(msg)

def create_message(message: str) -> str:
    return json.dumps({
        "type": "message",
        "message": message
    })

async def handler(ws: websockets.ServerConnection):
    print("client connected")
    try:
        raw = await ws.recv()
        parsed = parse_message(raw)

        if not parsed.get("nickname") or not parsed.get("type") == "join":
            await ws.send("Invalid join data")
            await ws.close()
            return
        
        ws.nickname = parsed["nickname"]
        clients.add(ws)

        await ws.send("Connected successfully")

        async for msg in ws:
            parsed = parse_message(msg)

            if parsed.get("type") == "message":
                for client in clients:
                    reply = create_message(f"[{ws.nickname}] {parsed.get("message")}")
                    await client.send(reply)

    except Exception as e:
        print("error")
        print(e)

    finally:
        print("client disconnected")
        clients.remove(ws)

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())