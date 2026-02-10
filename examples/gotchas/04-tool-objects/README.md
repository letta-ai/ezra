# Tool Object Access

## The Error

```
TypeError: 'Tool' object is not subscriptable
```

## Why It Happens

SDK objects are Pydantic models, not dicts. Use attribute access (dot notation).

## Fix

```python
# WRONG
tool['name']
tool['id']

# RIGHT
tool.name
tool.id
```

## Applies To

All SDK objects: agents, tools, blocks, messages, etc.

```python
agent.name      # not agent['name']
block.value     # not block['value']
msg.content     # not msg['content']
```
