import asyncio
import websockets

async def handle_messages(websocket):
    """Handles incoming messages from the server."""
    try:
        async for message in websocket:
            response = input(message)
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from server")

async def connect_to_server():
    """Connects to the WebSocket server and handles communication."""
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        await handle_messages(websocket)

# Start the client
asyncio.get_event_loop().run_until_complete(connect_to_server())
