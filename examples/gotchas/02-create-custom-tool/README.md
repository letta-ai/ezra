# Custom Tool Creation

## The Error

```
ImportError: No module named 'requests'
```
or
```
NameError: name 'os' is not defined
```

## Why It Happens

Letta tools run in a sandboxed environment. Your global imports and local
variables aren't available inside the tool function.

## Rules

1. **All imports inside the function** - The sandbox starts fresh each execution
2. **Use `os.getenv()` for secrets** - Don't pass API keys as function arguments
3. **Type hints + docstring required** - SDK auto-generates JSON schema from these
4. **Tools are always Python** - Even when using the TypeScript SDK

## Fix

```python
# WRONG - imports at top level
import requests

def my_tool(query: str, api_key: str) -> str:  # WRONG - secret as arg
    return requests.get(f"https://api.com?q={query}&key={api_key}").text

# RIGHT
def my_tool(query: str) -> str:
    """Search for something. Args: query: The search term."""
    import requests  # Import INSIDE
    import os
    api_key = os.getenv("MY_API_KEY")  # Secret from env
    return requests.get(f"https://api.com?q={query}", headers={"Authorization": api_key}).text
```

## Configuring Secrets

Set secrets at the agent level:
```python
client.agents.update(agent_id, tool_exec_environment_variables={"MY_API_KEY": "sk-..."})
```

Note: Secrets are agent-level, not per-user.
