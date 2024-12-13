import json
from codeforces.BlogClass import Blog



class MessageHandler:
  def __init__(self):
    pass
  
async def send_private_message(user_id, message):
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