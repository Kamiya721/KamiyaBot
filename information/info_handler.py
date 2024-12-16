# package: information.info_handler
import json
import websockets
import asyncio
import re
import os

NAPNEKO_WS_URL = "ws://127.0.0.1:3001/"

def load_json(permission_log_path):
  with open(permission_log_path, 'r') as f:
    return json.load(f)

def write_json(permission_log_path, permission_data):
  with open(permission_log_path, 'w') as f:
    json.dump(permission_data, f)

async def private_msg_handle(message):
  user_id = message.get('user_id')
  raw_message = message.get('raw_message')
  print(f"收到私聊消息：{raw_message}，来自用户 {user_id}")
  from information.msg_sender import send_private_message
  await send_private_message(user_id, "当前不允许私聊信息，您的消息已被忽略。")

async def add_alias(base_name, alias_name):
  alias_log_path = os.path.join(os.path.dirname(__file__), "Alias.json")
  try:
    alias_data = await asyncio.to_thread(load_json, alias_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Alias log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the alias log file.")
  
  if alias_name in alias_data:
    return False
  
  from permission.pms_check import ModuleCheck
  if not await ModuleCheck(base_name):
    raise ValueError(f"Module {base_name} not found.")
  alias_data[alias_name] = base_name
  await asyncio.to_thread(write_json, alias_log_path, alias_data)
  return True
  
async def find_alias(name):
  alias_log_path = os.path.join(os.path.dirname(__file__), "Alias.json")
  try:
    alias_data = await asyncio.to_thread(load_json, alias_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Alias log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the alias log file.")
  
  if name in alias_data:
    return alias_data[name]
  return None

async def group_msg_handle(message):
  user_id = message.get('user_id')
  group_id = message.get('group_id')
  raw_message = message.get('raw_message')
  from information.msg_sender import send_group_message
  
  match_res = re.match(r'^#(\w+)', raw_message)
  print(match_res)
  if not match_res:
    return 
  if await find_alias(match_res.group(1)):
    module_name = await find_alias(match_res.group(1))
  else:
    module_name = match_res.group(1)
  from permission.pms_check import CheckGroupPermission
  if not await CheckGroupPermission(group_id, user_id, module_name):
    await send_group_message(group_id, f"模块 {module_name} 未被允许使用。")
    return
  
  print(f"收到群聊消息：{raw_message}，来自用户 {user_id}，群组 {group_id}")
  
  if module_name == 'repeater':
    from repeater.repeat import repeat
    match_res = re.match(r'^r\s*#(\w+)\s+(.*)', raw_message)
    if not match_res:
      return
    data = match_res.group(2)
    res = await repeat(data)
    await send_group_message(group_id, res)
    
    
async def admin_msg_handle(message):
  from information.msg_sender import send_private_message
  admin_id = message.get('user_id')
  raw_message = message.get('raw_message')
  print("Admin message received: {}.".format(raw_message))
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
    if not group and message.get("message_type") == 'group':
      group = str(message.get("group_id"))
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
      if await SetUserPermission(user, module, True):
        await send_private_message(admin_id, f"已允许用户 {user} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"用户 {user} 已被允许使用模块 {module}。")
    if group:
      from permission.pms_set import SetGroupPermission
      if await SetGroupPermission(group, module, True):
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
    if not group and message.get("message_type") == 'group':
      group = str(message.get("group_id"))
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
      if await SetUserPermission(user, module, False):
        await send_private_message(admin_id, f"已禁止用户 {user} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"用户 {user} 已被禁止使用模块 {module}。")
    if group:
      from permission.pms_set import SetGroupPermission
      if await SetGroupPermission(group, module, False):
        await send_private_message(admin_id, f"已禁止群组 {group} 使用模块 {module}。")
      else:
        await send_private_message(admin_id, f"群组 {group} 已被禁止使用模块 {module}。")
  elif command[0] == 'alias':
    if len(command) == 2 and command[1] == '-h':
      await send_private_message(admin_id, "Usage: ! alias base_name alias_name")
      return
    if len(command) != 3:
      await send_private_message(admin_id, "Usage: ! alias base_name alias_name")
      return
    base_name = command[1]
    alias_name = command[2]
    if await add_alias(base_name, alias_name):
      await send_private_message(admin_id, f"已添加别名 {alias_name} -> {base_name}。")
    else:
      await send_private_message(admin_id, f"别名 {alias_name} 已存在。")
  elif command[0] == 'addmodule':
    if len(command) == 2 and command[1] == '-h':
      await send_private_message(admin_id, "Usage: ! addmodule module_name")
      return
    if len(command) != 2:
      await send_private_message(admin_id, "Usage: ! addmodule module_name")
      return
    module_name = command[1]
    from permission.pms_set import AddModule
    if await AddModule(module_name):
      await send_private_message(admin_id, f"已添加模块 {module_name}。")
    else:
      await send_private_message(admin_id, f"模块 {module_name} 已存在。")
  elif command[0] == 'removemodule':
    if len(command) == 2 and command[1] == '-h':
      await send_private_message(admin_id, "Usage: ! removemodule module_name")
      return
    if len(command) != 2:
      await send_private_message(admin_id, "Usage: ! removemodule module_name")
      return
    module_name = command[1]
    from permission.pms_set import RemoveModule
    if await RemoveModule(module_name):
      await send_private_message(admin_id, f"已删除模块 {module_name}。")
    else:
      await send_private_message(admin_id, f"模块 {module_name} 不存在。")

async def msg_handle(message):
  # print(message)
  from permission.pms_check import CheckAdmin
  # print(await CheckAdmin(message.get('user_id')))
  if await CheckAdmin(message.get('user_id')) and message.get('raw_message').startswith('! '):
    await admin_msg_handle(message)
    return
  
  if message.get("message_type") == 'private':
    await private_msg_handle(message)
  elif message.get("message_type") == 'group':
    await group_msg_handle(message)

async def info_handle(message):
  data = json.loads(message)
  # print("Received message: {}".format(data))
  if data.get('post_type') == 'message':
    await msg_handle(data)
    