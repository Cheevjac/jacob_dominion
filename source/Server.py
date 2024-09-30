import asyncio
import websockets

# Dictionary to store connected clients
clients = {}

async def broadcast(message):
    """Send a message to all connected clients."""
    if clients:
        print("Broadcasting message to all clients...")
        await asyncio.wait([client.send(message) for client in clients.values()])
    else:
        print("No clients to broadcast to.")

async def send_to_client(client_id, message):
    """Send a message to a specific client and wait for a response"""
    if client_id in clients:
        client = clients[client_id]
        try:
            await client.send(message)
            response = await client.recv()
            print(f"Response from client {client_id}: {response}")
            return response
        except websockets.exceptions.ConnectionClosed:
            print(f"Client {client_id} disconnected")
            del clients[client_id]
    else:
        print(f"Client {client_id} not found.")
        return None

async def handle_client(websocket, path):
    # Register the client
    client_id = len(clients) + 1
    clients[client_id] = websocket
    print(f"Client {client_id} connected")

    try:
        # Keep connection alive without responding to messages
        async for _ in websocket:
            pass # Ignore incoming message
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected")
    finally:
        # Unregister client
        del clients[client_id]

async def start_server():
    """Starts the WebSocket server."""
    print("WebSocket server started on ws://localhost:6789")
    server = await websockets.serve(handle_client, "localhost", 6789)
    await server.wait_closed()
    