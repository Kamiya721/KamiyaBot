# package: repeater.repeat

from jinja2 import Template
import asyncio

async def repeat(data):
  try:
    template = Template(data)
    output = template.render()
    return output
  except Exception as e:
    return f"Error: {e}"