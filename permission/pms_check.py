# package: permission.pms_check

import json
import asyncio
import os

def load_json(permission_log_path):
  with open(permission_log_path, 'r') as f:
    return json.load(f)

async def ModuleCheck(Module : str):
  log_path = os.path.join(os.path.dirname(__file__), "module_list.json")
  
  try:
    data = await asyncio.to_thread(load_json, log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found: {}".format(log_path))
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  
  Module = Module.lower()
  if Module in data:
    return True
  return False

async def CheckAdmin(user_id : str):
  permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")
  
  try:
    permission_data = await asyncio.to_thread(load_json, permission_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found: {}".format(permission_log_path))
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  user_id = str(user_id)
  if user_id in permission_data and permission_data[user_id].get('user_type') == 'admin':
    return True
  return False

async def CheckUserPermission(user_id : str, Module : str):
  permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")
  
  try:
    permission_data = await asyncio.to_thread(load_json, permission_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found: {}".format(permission_log_path))
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")

  if not await ModuleCheck(Module):
    raise ValueError(f"Module {Module} not found.")
  
  user_id = str(user_id)
  
  
  if user_id in permission_data and permission_data[user_id].get('user_type') == 'admin':
    return True
   
  if user_id not in permission_data:
    return False

  Module = Module.lower()
  if permission_data[user_id].get("allow").get(Module):
    return True
  
  return False

async def CheckGroupPermission(group_id : str, user_id : str, Module : str):
  group_permission_log_path = os.path.join(os.path.dirname(__file__), "Group_Permission.json")
  user_permission_log_path = os.path.join(os.path.dirname(__file__), "User_Permission.json")
  
  try:
    group_permission_data = await asyncio.to_thread(load_json, group_permission_log_path)
    user_permission_data = await asyncio.to_thread(load_json, user_permission_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  
  if not await ModuleCheck(Module):
    raise ValueError(f"Module {Module} not found.")
  
  user_id = str(user_id)
  group_id = str(group_id)
  
  if user_id in user_permission_data and user_permission_data[user_id].get('user_type') == 'admin':
    return True
  
  if group_id not in group_permission_data:
    return False
  Module = Module.lower()
  if user_id in user_permission_data and user_permission_data[user_id].get("deny").get(Module):
    return False
  if Module in group_permission_data[group_id].get("allow"):
    return True
  return False