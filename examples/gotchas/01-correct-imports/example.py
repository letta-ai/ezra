"""Correct way to import and initialize the Letta client.

Common mistake: `from letta import Letta` (wrong package).
The SDK package is `letta-client`, not `letta`.
"""

import os

# CORRECT - SDK 1.0+
from letta_client import Letta

# Initialize with API key (Letta Cloud)
client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# For self-hosted servers:
# client = Letta(base_url="http://localhost:8283")

# Verify connection by listing agents
agents = client.agents.list(limit=1)
print(f"Connected! Found {len(agents.items)} agent(s)")
