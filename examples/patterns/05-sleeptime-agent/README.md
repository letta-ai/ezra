# Sleeptime Agent

## Pattern

Agent with background memory processing that runs between conversations.

```
User messages ──► Agent responds ──► Sleeptime agent reviews & updates memory
```

## When to Use

- Agents that need to consolidate knowledge from conversations
- Long-running agents that accumulate context over time
- Agents where memory quality matters more than response speed

## Setup

```python
agent = client.agents.create(
    ...,
    enable_sleeptime=True,
)
```

## Configure Frequency

```python
# MUST nest inside manager_config (top-level silently ignored)
client.groups.update(
    agent.multi_agent_group.id,
    manager_config={
        "manager_type": "sleeptime",
        "sleeptime_agent_frequency": 10,  # Every 10 messages
    },
)
```

## How It Works

1. Agent responds to user messages normally
2. After threshold met (frequency + interval), sleeptime agent activates
3. Sleeptime reviews conversation transcripts (doesn't re-execute tools)
4. Updates shared memory blocks based on analysis
5. Changes visible to all conversations on next context compilation

## Important Notes

- Triggers on TOTAL messages across ALL conversations (not per-conversation)
- Both `interval_seconds` and `min_messages` must be met
- Sleeptime agent uses the same model as the main agent by default
