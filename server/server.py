import asyncio
import websockets
from websockets.asyncio.server import serve
from websockets.asyncio.server import ServerConnection

import json

clients: set[websockets.ServerConnection] = set()

def parse_message(msg: str) -> dict:
    try:
        parsed = json.loads(msg)
        if type(parsed) != dict:
            return None
        return parsed
    
    except:
        return None


def create_message(message: str) -> str:
    return json.dumps({
        "type": "message",
        "message": message
    })

async def handler(ws: ServerConnection):
    print("client connected")
    try:
        raw = await ws.recv()
        parsed = parse_message(raw)


        if not parsed:
            await ws.close(websockets.CloseCode.INVALID_DATA)
            return
        

        if not parsed.get("nickname") or not parsed.get("type") == "join":
            print("client sent invalid connection data")
            await ws.close(websockets.CloseCode.INVALID_DATA)
            return
        
        ws.nickname = parsed["nickname"]
        clients.add(ws)

        await ws.send(create_message("Connected succesfully"))

        async for msg in ws:
            parsed = parse_message(msg)

            if not parsed:
                await ws.close(websockets.CloseCode.INVALID_DATA)
                return

            if parsed.get("type") == "message":
                for client in clients:
                    if client.state == websockets.State.OPEN:
                        reply = create_message(f"[{ws.nickname}] {parsed.get("message")}")
                        await client.send(reply)

    # except websockets.exceptions.ConnectionClosedOK as closeException:
    #     pass

    finally:
        print("client disconnected")
        clients.discard(ws)

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())