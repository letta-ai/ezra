# Streaming Responses

## Pattern

Real-time token streaming via SSE (Server-Sent Events).

## When to Use

- Chat UIs that need to show tokens as they arrive
- Long responses where users shouldn't wait for completion
- Any latency-sensitive application

## Key Methods

```python
# Non-streaming (waits for full response)
response = client.agents.messages.create(agent_id, messages=[...])

# Streaming (yields chunks as they arrive)
stream = client.agents.messages.create_stream(agent_id, messages=[...])
for chunk in stream:
    if chunk.message_type == "assistant_message":
        print(chunk.content, end="")
```

## Cloudflare Timeout Prevention

For requests that may take > 2 minutes (complex tool chains, slow models):

```python
stream = client.agents.messages.create_stream(
    agent_id=agent.id,
    messages=[...],
    include_pings=True,  # Pings every 30s keep connection alive
)
```

Without `include_pings=True`, Cloudflare returns 524 errors after ~100 seconds.

## Important Notes

- Streaming is token-level for assistant messages
- Tool calls and tool returns also appear in the stream
- Ollama only supports agent-step streaming (not token-level)
