# Ezra Monitor

Monitor and examine ezra-prime's activities to propose memory block updates.

## Purpose

Self-reflection tool that analyzes ezra-prime's Discord support conversations to:
- Identify recurring patterns and issues
- Detect knowledge gaps from repeated questions
- Propose updates to memory blocks based on learnings
- Track team corrections and user feedback

## Scripts

### `scripts/fetch-recent.sh`
Fetches recent conversations and messages from ezra-prime.

```bash
./scripts/fetch-recent.sh [hours] [limit]
# Default: last 24 hours, 50 messages
```

### `scripts/analyze-patterns.sh`
Analyzes fetched messages for patterns.

```bash
./scripts/analyze-patterns.sh <messages.json>
# Outputs: recurring topics, unanswered questions, corrections
```

### `scripts/propose-updates.sh`
Generates proposed memory block updates based on analysis.

```bash
./scripts/propose-updates.sh <analysis.json>
# Outputs: suggested edits to specific memory blocks
```

## Environment

Requires:
- `LETTA_API_KEY` - API access
- `EZRA_PRIME_AGENT_ID` - Target agent (default: agent-57ce3ea1-72ad-43e5-a444-7e3724f706e8)

## Workflow

1. Run fetch-recent.sh to download conversation data
2. Run analyze-patterns.sh to identify learnings
3. Run propose-updates.sh to generate memory edit suggestions
4. Review and apply updates manually or via API
