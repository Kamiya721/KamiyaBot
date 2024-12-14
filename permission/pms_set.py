import json
import asyncio
import os

async def SetUserPermission(user_id, Module, isallow):
  permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")

  try:
    async with asyncio.to_thread(open, permission_log_path, 'r') as f:
      permission_data = json.load(f)
  except FileNotFoundError:
    raise FileNotFoundError(f"Permission log file not found: {permission_log_path}")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")

  if user_id in permission_data and permission_data[user_id].get('user_type') == 'admin':
    return False

  if user_id not in permission_data:
    permission_data[user_id] = {'user_type': 'user', 'allow': [], 'disallow': []}

  Module = Module.lower()

  if isallow:
    if Module not in permission_data[user_id]['allow']:
      permission_data[user_id]['allow'].append(Module)
    if Module in permission_data[user_id]['disallow']:
      permission_data[user_id]['disallow'].remove(Module)
  else:
    if Module not in permission_data[user_id]['disallow']:
      permission_data[user_id]['disallow'].append(Module)
    if Module in permission_data[user_id]['allow']:
      permission_data[user_id]['allow'].remove(Module)

  async with asyncio.to_thread(open, permission_log_path, 'w') as f:
    json.dump(permission_data, f)

  return True

async def SetGroupPermission(group_id, Module, isallow):
  group_permission_log_path = os.path.join(os.path.dirname(__file__), "Group_Permission.json")

  try:
    async with asyncio.to_thread(open, group_permission_log_path, 'r') as f:
      group_permission_data = json.load(f)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")

  if group_id not in group_permission_data:
    group_permission_data[group_id] = {'allow': [], 'disallow': []}

  Module = Module.lower()

  if isallow:
    if Module not in group_permission_data[group_id]['allow']:
      group_permission_data[group_id]['allow'].append(Module)
    if Module in group_permission_data[group_id]['disallow']:
      group_permission_data[group_id]['disallow'].remove(Module)
  else:
    if Module not in group_permission_data[group_id]['disallow']:
      group_permission_data[group_id]['disallow'].append(Module)
    if Module in group_permission_data[group_id]['allow']:
      group_permission_data[group_id]['allow'].remove(Module)

  async with asyncio.to_thread(open, group_permission_log_path, 'w') as f:
    json.dump(group_permission_data, f)

  return True
