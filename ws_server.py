import asyncio
import json
import threading
from websockets.server import serve

# Shared state (read by overlay, written by WS server)
browser_state = {
    "Chrome": []
}

browser_state_lock = threading.Lock()

async def handle_client(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)

            # Expected format:
            # {
            #   "browser": "Chrome",
            #   "tabs": ["ChatGPT – Google", "LeetCode"]
            # }

            browser = data.get("browser")
            tabs = data.get("tabs", [])

            if browser:
                with browser_state_lock:
                    browser_state[browser] = tabs
                    # print("📥 Browser data received:", browser, tabs)

        except json.JSONDecodeError:
            print("Invalid JSON received")

async def run_server():
    async with serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

def start_ws_server():
    asyncio.run(run_server())