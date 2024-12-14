# package: codeforces.CFclass
import asyncio
import json
import websockets
import aiohttp


class CFUser :
  def __init__(self, cf_id, rating):
    self.cf_id = cf_id
    self.rating = rating
  