# package: information.info_handler
import json
import websockets
import asyncio

NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

async def info_handle(message):
  data = json.loads(message)
  