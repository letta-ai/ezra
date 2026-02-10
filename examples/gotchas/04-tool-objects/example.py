"""Correct way to access tool object properties.

Tool objects use dot notation (attribute access), not dict subscripting.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# List tools
tools = client.tools.list()

for tool in tools.items:
    # RIGHT: dot notation
    print(f"Tool: {tool.name}")
    print(f"  ID: {tool.id}")
    print(f"  Schema: {tool.json_schema}")
    print()

    # WRONG: dict subscripting
    # tool['name']  -> TypeError: 'Tool' object is not subscriptable
    # tool['id']    -> TypeError: 'Tool' object is not subscriptable
