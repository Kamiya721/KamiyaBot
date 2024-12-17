# package: codeforces.UserSearch
import asyncio
import json
import websockets
import aiohttp
import base64
import os

async def get_user_info(username):
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"https://codeforces.com/api/user.info?handles={username}&checkHistoricHandles=false") as response:
        data = await response.text()
        return json.loads(data)
  except Exception as e:
    print(e)
    return None

ranking = {
  'newbie': 'Newbie',
  'pupil': 'Pupil',
  'specialist': 'Spelist',
  'expert': 'Expert',
  'candidate master': 'CM',
  'master': 'Master',
  'international master': 'IM',
  'grandmaster': 'GM',
  'international grandmaster': 'IGM',
  'legendary grandmaster': 'LGM',
  'unrated': 'Unrated',
  'tourist': 'Tourist'
}

async def PrintImage(username):
  try:
    data = await get_user_info(username)
    # print(data)
    if data['status'] == 'FAILED':
      print('User not found')
      return None
    if 'rating' in data['result'][0]:
      rating = data['result'][0]['rating']
      max_rating = data['result'][0]['maxRating']
      rank = data['result'][0]['rank']
    else:
      rating = 0
      max_rating = 0
      rank = "unrated"
    handle = data['result'][0]['handle']
    stars = data['result'][0]['friendOfCount']
    avatar = data['result'][0]['titlePhoto']
    rank = ranking[rank]
    from codeforces.image_painter import generate_codeforces_card
    generate_codeforces_card(
      username=handle,
      rating=rating,
      max_rating=max_rating,
      level=rank,
      stars=stars,
      avatar_url=avatar,
      output_path=f"{handle}_card.png"
    )
    print(f"Codeforces card saved to {handle}_card.png")
    with open(f"{handle}_card.png", "rb") as image_file:
          # 使用 base64 模块编码
      encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    os.system(f"rm {handle}_card.png")
    return [
      {
        "type": "image",
        "data": {
          "file": "base64://" + encoded_string
        }
      }
    ]
  except Exception as e:
    print(e)
    return None