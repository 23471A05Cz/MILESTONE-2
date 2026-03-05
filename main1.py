from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = []

@app.get("/")
async def get():
    with open("milestone2.html") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients.append((websocket, username))

    join_msg = f"{username} joined the chat"
    await broadcast(join_msg)

    try:
        while True:
            data = await websocket.receive_text()
            msg = f"{username}: {data}"
            await broadcast(msg)

    except WebSocketDisconnect:
        clients.remove((websocket, username))
        leave_msg = f"{username} left the chat"
        await broadcast(leave_msg)


async def broadcast(message: str):
    for client, name in clients:
        await client.send_text(message)