# Update Not Modify

## The Error

```
AttributeError: 'Agents' object has no attribute 'modify'
```

## Why It Happens

SDK 1.0 renamed `.modify()` to `.update()` across all resources.
Old tutorials and code samples may still reference `.modify()`.

## Fix

```python
# WRONG (pre-1.0)
client.agents.modify(agent_id, name="new_name")

# RIGHT (SDK 1.0+)
client.agents.update(agent_id, name="new_name")
```

## Applies To

All resources:
- `client.agents.update()`
- `client.agents.blocks.update()`
- `client.tools.update()`

## Migration Guide

https://docs.letta.com/api-reference/sdk-migration-guide/#method-modify-does-not-exist
