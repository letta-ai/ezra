# Multi-Agent Coordination

## Pattern

Client-side orchestration with shared memory blocks.

```
Orchestrator (your code)
    ├──► Agent A (researcher) ──┐
    │                            ├──► Shared blocks (task_board, findings)
    └──► Agent B (writer) ──────┘
```

## When to Use

- Specialized agents for different subtasks
- Pipelines where output from one agent feeds into another
- When you need explicit control over agent execution order

## Why Client-Side?

Letta team recommends client-side orchestration over server-side groups:
- Full control over execution flow
- Explicit error handling
- Can run agents in parallel or sequential
- Easier to debug

## Key Concepts

- **Shared blocks**: Same block attached to multiple agents
- **Block as message bus**: Agents write results to shared blocks
- **Sequential handoff**: Orchestrator controls which agent runs when
- **Changes propagate**: Updates visible on next context compilation

## Important Notes

- Prefer `memory_insert` for concurrent writes (append-safe)
- Detach shared blocks before deleting agents
- Each agent runs independently (no direct agent-to-agent calls)
