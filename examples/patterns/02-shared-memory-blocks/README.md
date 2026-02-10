# Shared Memory Blocks

## Pattern

Multiple agents sharing a single memory block.

```
Agent A ──► reads/writes ──┐
                            ├──► Shared Block
Agent B ──► reads/writes ──┘
```

## When to Use

- Fleet of agents that need consistent knowledge (company policies, product info)
- Multi-agent systems where agents need to coordinate
- Single source of truth across agent instances

## Key Concepts

- **Independent blocks**: Create with `client.blocks.create()` (not tied to any agent)
- **Attach**: `client.agents.blocks.attach(agent_id, block_id=block_id)`
- **Detach**: `client.agents.blocks.detach(agent_id, block_id=block_id)`
- **Same block ID**: Both agents reference the exact same block object
- **Propagation**: Changes visible on next context compilation (not instant mid-turn)

## Concurrency Notes

- `memory_insert`: Most robust for concurrent writes (append-only)
- `memory_replace`: Can fail in race conditions (exact string match)
- `memory_rethink`: Last-writer-wins (full rewrite)
- For safety, prefer one writer + many readers
