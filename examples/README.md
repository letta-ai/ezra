# Letta Examples & Pattern Library

Runnable, tested examples covering common SDK gotchas and architecture patterns.
Every example is verified against the live Letta API.

## Gotchas

Quick fixes for the most common SDK mistakes.

| # | Example | Error You'll Hit |
|---|---------|-----------------|
| 01 | [Correct imports](gotchas/01-correct-imports/) | `ModuleNotFoundError: No module named 'letta'` |
| 02 | [Custom tool creation](gotchas/02-create-custom-tool/) | ImportError in sandbox, missing secrets |
| 03 | [Pagination](gotchas/03-pagination/) | Missing results, `TypeError: no len()` |
| 04 | [Tool objects](gotchas/04-tool-objects/) | `TypeError: 'Tool' object is not subscriptable` |
| 05 | [Message roles](gotchas/05-message-roles/) | `422: role='tool' not allowed` |
| 06 | [Update not modify](gotchas/06-update-not-modify/) | `AttributeError: no attribute 'modify'` |
| 07 | [Sleeptime frequency](gotchas/07-sleeptime-frequency/) | Frequency change silently ignored |

## Patterns

Architecture recipes for real applications.

| # | Pattern | What It Shows |
|---|---------|--------------|
| 01 | [Multi-user conversations](patterns/01-multi-user-conversations/) | Parallel user sessions on one agent |
| 02 | [Shared memory blocks](patterns/02-shared-memory-blocks/) | Cross-agent memory sharing |
| 03 | [Custom tool with secrets](patterns/03-custom-tool-with-secrets/) | Full tool creation flow with env secrets |
| 04 | [Streaming responses](patterns/04-streaming-responses/) | SSE streaming with keepalive pings |
| 05 | [Sleeptime agent](patterns/05-sleeptime-agent/) | Background memory processing |
| 06 | [Dynamic context](patterns/06-dynamic-context/) | Runtime block attach/detach |
| 07 | [Multi-agent coordination](patterns/07-multi-agent-coordination/) | Client-side orchestration with shared state |

## Running

```bash
# Install dependencies
pip install letta-client pytest

# Set API key
export LETTA_API_KEY="your-key-here"

# Run all examples
pytest examples/ -v

# Run specific category
pytest examples/gotchas/ -v
pytest examples/patterns/ -v
```

## Structure

Each example contains:
- `example.py` - Working Python example
- `example.ts` - Working TypeScript example
- `README.md` - What this solves, common error, correct pattern
- `test_example.py` - Automated test that verifies the example works
