import json
import asyncio
import os
from permission.pms_check import ModuleCheck

def load_json(permission_log_path):
  try:
    with open(permission_log_path, 'r') as f:
      return json.load(f)
  except Exception as e:
    print(f"Error loading JSON: {e}")
    return {}

def write_json(permission_log_path, permission_data):
  try:
    with open(permission_log_path, 'w') as f:
      json.dump(permission_data, f)
  except Exception as e:
    print(f"Error writing JSON: {e}")

async def SetUserPermission(user_id : str, Module : str, isallow : bool):
  permission_log_path = os.path.join(os.path.dirname(__file__), os.path.expanduser("~/DataStore/User_Permission.json"))

  try:
    permission_data = await asyncio.to_thread(load_json, permission_log_path)
  except FileNotFoundError:
    raise FileNotFoundError(f"Permission log file not found: {permission_log_path}")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  except Exception as e:
    print(f"Error in SetUserPermission: {e}")
    return False

  try:
    if not await ModuleCheck(Module):
      raise ValueError(f"Module {Module} not found.")
  except Exception as e:
    print(f"Error in ModuleCheck: {e}")
    return False
  
  user_id = str(user_id)

  if user_id in permission_data and permission_data[user_id].get('user_type') == 'admin':
    return False

  if user_id not in permission_data:
    permission_data[user_id] = {'user_type': 'user', 'allow': [], 'deny': []}

  Module = Module.lower()

  if isallow:
    if Module not in permission_data[user_id]['allow']:
      permission_data[user_id]['allow'].append(Module)
    if Module in permission_data[user_id]['deny']:
      permission_data[user_id]['deny'].remove(Module)
  else:
    if Module not in permission_data[user_id]['deny']:
      permission_data[user_id]['deny'].append(Module)
    if Module in permission_data[user_id]['allow']:
      permission_data[user_id]['allow'].remove(Module)

  try:
    await asyncio.to_thread(write_json, permission_log_path, permission_data)
  except Exception as e:
    print(f"Error writing JSON in SetUserPermission: {e}")
    return False

  return True

async def SetGroupPermission(group_id : str, Module : str, isallow : bool):
  group_permission_log_path = os.path.join(os.path.dirname(__file__), os.path.expanduser("~/DataStore/Group_Permission.json"))

  try:
    group_permission_data = await asyncio.to_thread(load_json, group_permission_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Permission log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the permission log file.")
  except Exception as e:
    print(f"Error in SetGroupPermission: {e}")
    return False

  try:
    if not await ModuleCheck(Module):
      raise ValueError(f"Module {Module} not found.")
  except Exception as e:
    print(f"Error in ModuleCheck: {e}")
    return False
  
  group_id = str(group_id)
  
  if group_id not in group_permission_data:
    group_permission_data[group_id] = {'allow': [], 'deny': []}

  Module = Module.lower()

  if isallow:
    if Module not in group_permission_data[group_id]['allow']:
      group_permission_data[group_id]['allow'].append(Module)
    if Module in group_permission_data[group_id]['deny']:
      group_permission_data[group_id]['deny'].remove(Module)
  else:
    if Module not in group_permission_data[group_id]['deny']:
      group_permission_data[group_id]['deny'].append(Module)
    if Module in group_permission_data[group_id]['allow']:
      group_permission_data[group_id]['allow'].remove(Module)

  try:
    await asyncio.to_thread(write_json, group_permission_log_path, group_permission_data)
  except Exception as e:
    print(f"Error writing JSON in SetGroupPermission: {e}")
    return False

  return True

async def AddModule(module : str):
  module_log_path = os.path.join(os.path.dirname(__file__), os.path.expanduser("~/DataStore/module_list.json"))

  try:
    module_data = await asyncio.to_thread(load_json, module_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Module log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the module log file.")
  except Exception as e:
    print(f"Error in AddModule: {e}")
    return False

  if module in module_data:
    return False

  module_data.append(module)

  try:
    await asyncio.to_thread(write_json, module_log_path, module_data)
  except Exception as e:
    print(f"Error writing JSON in AddModule: {e}")
    return False

  return True

async def RemoveModule(module : str):
  module_log_path = os.path.join(os.path.dirname(__file__), os.path.expanduser("~/DataStore/module_list.json"))

  try:
    module_data = await asyncio.to_thread(load_json, module_log_path)
  except FileNotFoundError:
    raise FileNotFoundError("Module log file not found.")
  except json.JSONDecodeError:
    raise ValueError("Error decoding the module log file.")
  except Exception as e:
    print(f"Error in RemoveModule: {e}")
    return False

  if module not in module_data:
    return False

  module_data.remove(module)

  try:
    await asyncio.to_thread(write_json, module_log_path, module_data)
  except Exception as e:
    print(f"Error writing JSON in RemoveModule: {e}")
    return False

  return True