# Custom Tool with Secrets

## Pattern

Full tool lifecycle: define, register, attach secrets, use.

```
Define function → Register tool → Create agent → Set secrets → Agent uses tool
```

## Key Rules

1. **Imports inside function** - Sandbox starts fresh each execution
2. **`os.getenv()` for secrets** - Never pass secrets as function arguments
3. **Type hints + docstring** - SDK auto-generates JSON schema
4. **Each arg needs a docstring description** - Will fail schema generation otherwise
5. **Source code as string** - Pass to `client.tools.create(source_code=...)`

## Setting Secrets

```python
# At agent creation
agent = client.agents.create(
    ...,
    tool_exec_environment_variables={"MY_API_KEY": "sk-..."},
)

# Or update later
client.agents.update(
    agent_id,
    tool_exec_environment_variables={"MY_API_KEY": "sk-..."},
)
```

## Important Notes

- Secrets are **agent-level**, not per-user or per-tool
- Tools are **always Python**, even from TypeScript SDK
- `client` variable is pre-injected on Letta Cloud (for calling Letta API from tools)
- pip/letta_client not available in sandbox - use HTTP for external calls
