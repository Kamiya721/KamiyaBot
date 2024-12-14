import asyncio
import json
import websockets
import platform
import os
import requests
import aiohttp
from information.info_handler import info_handle

NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

async def main():
  async with websockets.connect(NAPNEKO_WS_URL) as ws:
    print("已连接到 NapNeko WebSocket 服务")
    while True:
      try:
        message = await ws.recv()
        await info_handle(message)                
      except websockets.ConnectionClosed:
        print("连接关闭，正在尝试重连...")
        break

if __name__ == "__main__":
  asyncio.run(main())