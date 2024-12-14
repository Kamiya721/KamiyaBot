# package: permission.pms_check

import json
import asyncio
import os

async def CheckUserPermission(user_id, Module):
  permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")
  
  try:
    async with asyncio.to_thread(permission_log_path, 'r') as f:
      permission_data = await json.load(f)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found: {}".format(permission_log_path))
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  
  if permission_data[user_id].get('user_type') == 'admin':
    return True
   
  if user_id not in permission_data:
    return False

  Module = Module.lower()
  if permission_data[user_id].get("allow").get(Module):
    return True
  
  return False

async def CheckGroupPermission(group_id, User_id, Module):
  group_permission_log_path = os.path.join(os.path.dirname(__file__), "Group_Permission.json")
  user_permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")
  
  try:
    async with asyncio.to_thread(group_permission_log_path, 'r') as f:
      group_permission_data = await json.load(f)
    async with asyncio.to_thread(user_permission_log_path, 'r') as f:
      user_permission_data = await json.load(f)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  
  if user_permission_data[User_id].get('user_type') == 'admin':
    return True
  
  if group_id not in group_permission_data:
    return False
  Module = Module.lower()
  if User_id in user_permission_data and user_permission_data[User_id].get("disallow").get(Module):
    return False
  if Module in group_permission_data[group_id].get("allow"):
    return True
  return False