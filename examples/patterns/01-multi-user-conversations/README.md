# Multi-User Conversations

## Pattern

One agent, multiple users, each with their own conversation.

```
User A ──► Conversation A ──┐
                             ├──► Agent (shared memory)
User B ──► Conversation B ──┘
```

## When to Use

- Chat apps where multiple users talk to the same agent
- Support bots handling concurrent requests
- Any scenario where users need isolated sessions but shared agent knowledge

## Key Concepts

- **Conversations API**: `client.conversations.create(agent_id=...)`
- **Isolation**: Users can't see each other's messages
- **Shared memory**: Agent's memory blocks are shared across all conversations
- **True parallelism**: Different conversations run concurrently
- **Blocking**: Only within a single conversation (can't send while processing)

## Important Notes

- Sleeptime triggers based on TOTAL messages across ALL conversations
- Memory updates from one conversation are visible in others (next context compile)
- Create one `conversation_id` per user session
