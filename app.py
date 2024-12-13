import asyncio
import json
import websockets
import platform
import os
import requests
import aiohttp

async def get_cf_rating(user_id):
    codeforces_url = f'https://codeforces.com/api/user.rating?handle={user_id}'
    try:
        
    # 使用 aiohttp 发送异步请求
        async with aiohttp.ClientSession() as session:
            async with session.get(codeforces_url) as res:
                data = await res.json()  # 获取 JSON 数据
    except Exception as e:
        print(f'Error: {e}')
        return {'failed', "Error."}
            
    if data.get("status") != "OK":
        return {'failed', "Not Found."}
    
    if len(data.get("result")) == 0:
        return {'failed', "Unrated."}
    
    return {'ok', data.get('result')[-1].get('newRating')}  # 获取最新的 rating


# 配置 NapNeko WebSocket 地址
NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

# 消息处理逻辑
async def handle_message(message):
    # 将接收到的消息解析为字典
    data = json.loads(message)

    # 判断是否为消息事件
    if data.get("post_type") == "message":
        message_type = data.get("message_type")
        raw_message = data.get("raw_message")
        user_id = data.get("user_id")
        sender_nickname = data.get("sender", {}).get("nickname", "未知昵称")

        # 私聊消息
        if message_type == "private":
            pass
            #print(f"收到私聊消息：{raw_message}，来自用户 {user_id}（昵称：{sender_nickname}）")
            #await send_private_message(user_id, f"你发送的消息是：{raw_message}")

        # 群聊消息
        elif message_type == "group":
            group_id = data.get("group_id")
            print(f"收到群聊消息：{raw_message}，来自群 {group_id} 的用户 {user_id}（昵称：{sender_nickname}）")
            # print(raw_message[:4])
            if raw_message.startswith('#cf '):
               cf_id = raw_message[4:]
               print(f'{user_id} 请求的 CF ID 是：{cf_id}')
               cf_res = await get_cf_rating(cf_id)
               if cf_res == 'Not Found.' or cf_res == 'Unrated.':
                  await send_group_message(group_id, cf_res)
               else :
                  await send_group_message(group_id, f"codeforces ID 为 {cf_id} 的用户的最新 rating 为：{cf_res}")
                  
# 发送私聊消息
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

# 发送群聊消息
async def send_group_message(group_id, message):
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
# 发送消息函数
async def send_message(user_id, message):
    # 构造发送消息的 payload，根据 API 文档定义
    payload = {
        "action": "send_message",
        "data": {
            "receiver_id": user_id,
            "message": message,
        }
    }

    # 通过 WebSocket 发送
    async with websockets.connect(NAPNEKO_WS_URL) as ws:
        await ws.send(json.dumps(payload))
        response = await ws.recv()
        print(f"发送消息的响应：{response}")

# 主函数，用于连接 WebSocket 并处理消息
async def main():
    async with websockets.connect(NAPNEKO_WS_URL) as ws:
        print("已连接到 NapNeko WebSocket 服务")
        while True:
            try:
                # 等待接收消息
                message = await ws.recv()
               #  print(f"收到消息：{message}")

                # 处理消息
                await handle_message(message)
            except websockets.ConnectionClosed:
                print("连接关闭，正在尝试重连...")
                break

# 启动 WebSocket 监听
if __name__ == "__main__":
    asyncio.run(main())