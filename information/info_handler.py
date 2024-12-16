# package: information.info_handler
import json
import websockets
import asyncio

NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

async def private_msg_handle(message):
  user_id = message.get('user_id')
  raw_message = message.get('raw_message')
  from information.msg_sender import send_private_message
  await send_private_message(user_id, "当前不允许私聊信息，您的消息已被忽略。")

async def group_msg_handle(message):
  user_id = message.get('user_id')
  group_id = message.get('group_id')
  raw_message = message.get('raw_message')
  from information.msg_sender import send_group_message
  

async def admin_msg_handle(message):
  from information.msg_sender import send_private_message
  admin_id = message.get('user_id')
  raw_message = message.get('raw_message')
  command = raw_message[2:].split(' ')
  if command[0] == 'allow':
    user = None; group = None; module = None
    if len(command) == 2 and command[1] == '-h':
      await send_private_message(admin_id, "Usage: ! allow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]")
      return
    for i in range(1, len(command)):
      if command[i] == '-u' or command[i] == '--user':
        user = command[i+1]
      elif command[i] == '-g' or command[i] == '--group':
        group = command[i+1]
      elif command[i] == '-m' or command[i] == '--module':
        module = command[i+1]
        
    if not user and not group:
      await send_private_message(admin_id, '''Usage: ! allow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]
                                 请指定用户或群组。''')
      return
    if not module:
      await send_private_message(admin_id, '''Usage: ! allow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]
                                 请指定模块。''')
      return
    if user:
      from permission.pms_set import SetUserPermission
      if SetUserPermission(user, module, True):
        await send_private_message(admin_id, f"已允许用户 {user} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"用户 {user} 已被允许使用模块 {module}。")
    if group:
      from permission.pms_set import SetGroupPermission
      if SetGroupPermission(group, module, True):
        await send_private_message(admin_id, f"已允许群组 {group} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"群组 {group} 已被允许使用模块 {module}。")
  elif command[0] == 'disallow':
    user = None; group = None; module = None
    if len(command) == 2 and command[1] == '-h':
      await send_private_message(admin_id, "Usage: ! disallow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]")
      return
    for i in range(1, len(command)):
      if command[i] == '-u' or command[i] == '--user':
        user = command[i+1]
      elif command[i] == '-g' or command[i] == '--group':
        group = command[i+1]
      elif command[i] == '-m' or command[i] == '--module':
        module = command[i+1]
        
    if not user and not group:
      await send_private_message(admin_id, '''Usage: ! disallow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]
                                 请指定用户或群组。''')
      return
    if not module:
      await send_private_message(admin_id, '''Usage: ! disallow [-u/--user user_id] [-g/--group group_id] [-m/--module module_name]
                                 请指定模块。''')
      return
    if user:
      from permission.pms_set import SetUserPermission
      if SetUserPermission(user, module, False):
        await send_private_message(admin_id, f"已禁止用户 {user} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"用户 {user} 已被禁止使用模块 {module}。")
    if group:
      from permission.pms_set import SetGroupPermission
      if SetGroupPermission(group, module, False):
        await send_private_message(admin_id, f"已禁止群组 {group} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"群组 {group} 已被禁止使用模块 {module}。")
  

async def msg_handle(message):
  from permission.pms_check import CheckAdmin
  if await CheckAdmin(message.get('user_id')) and message.get('raw_message').startswith('! '):
    await admin_msg_handle(message)
    return
  match message.get("message_tpye"):
    case 'private':
      await private_msg_handle(message)
    case 'group':
      await group_msg_handle(message)

async def info_handle(message):
  data = json.loads(message)
  if data.get('post_type') == 'message':
    await msg_handle(data)
    