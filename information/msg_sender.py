# package: information.msg_sender
import websockets
import json
import asyncio

NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

async def send_private_message(user_id, message):
  try:
    payload = {
      "action": "send_private_msg",
      "params": {
        "user_id": user_id,
        "message": message
      }
    }
    async with websockets.connect(NAPNEKO_WS_URL) as ws:
      await ws.send(json.dumps(payload))
      response = await ws.recv()
      print(f"私聊消息发送响应：{response}")
  except Exception as e:
    print(f"Error sending private message: {e}")

async def send_group_message(group_id, message):
  try:
    payload = {
      "action": "send_group_msg",
      "params": {
        "group_id": group_id,
        "message": message
      }
    }
    async with websockets.connect(NAPNEKO_WS_URL) as ws:
      await ws.send(json.dumps(payload))
      response = await ws.recv()
      print(f"群聊消息发送响应：{response}")
  except Exception as e:
    print(f"Error sending group message: {e}")