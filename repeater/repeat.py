# package: repeater.repeat

from jinja2 import Template, Environment
import asyncio

async def repeat(data):
  try:
    env = Environment(
      autoescape=True
    )
    env.globals = {}
    template = env.from_string(data)
    output = template.render()
    return output
  except Exception as e:
    return f"Error: {e}"