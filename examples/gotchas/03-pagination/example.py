"""Correct way to paginate through Letta API results.

SDK 1.0+ uses cursor-based pagination. Results come in a page object
with an .items property - you can't iterate the page directly.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Basic pagination ---

# Results come in a page object with .items
page = client.agents.list(limit=5)
print(f"Got {len(page.items)} agents")

# WRONG: len(page) - page object has no len()
# WRONG: for agent in page - can't iterate page directly
# RIGHT:
for agent in page.items:
    print(f"  {agent.name} ({agent.id})")

# --- Cursor-based pagination ---

# Use before/after cursors for navigating pages
first_page = client.agents.list(limit=3)
print(f"\nFirst page: {len(first_page.items)} agents")

if first_page.items:
    # Get next page using the last item's ID as cursor
    last_id = first_page.items[-1].id
    second_page = client.agents.list(limit=3, after=last_id)
    print(f"Second page: {len(second_page.items)} agents")

# --- Iterating all results ---

def list_all_agents(client, limit=10):
    """Fetch all agents using cursor pagination."""
    all_agents = []
    after = None

    while True:
        kwargs = {"limit": limit}
        if after:
            kwargs["after"] = after

        page = client.agents.list(**kwargs)
        if not page.items:
            break

        all_agents.extend(page.items)
        after = page.items[-1].id

        if len(page.items) < limit:
            break  # Last page

    return all_agents

agents = list_all_agents(client)
print(f"\nTotal agents: {len(agents)}")
