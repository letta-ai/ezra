# Pagination

## The Error

```
TypeError: object of type 'SyncPage' has no len()
```
or results silently missing.

## Why It Happens

SDK 1.0 returns page objects, not plain lists. You need to access `.items`.

## Fix

```python
# WRONG
agents = client.agents.list(limit=10)
for agent in agents:        # Can't iterate page directly
    print(agent.name)

# RIGHT
page = client.agents.list(limit=10)
for agent in page.items:     # Access .items
    print(agent.name)
```

## Cursor Pagination

For navigating large result sets:

```python
after = None
while True:
    page = client.agents.list(limit=10, after=after)
    if not page.items:
        break
    for agent in page.items:
        process(agent)
    after = page.items[-1].id
    if len(page.items) < 10:
        break
```

## Applies To

All list endpoints: `agents.list()`, `tools.list()`, `blocks.list()`, etc.
