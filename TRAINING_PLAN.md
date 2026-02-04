# Ezra Training Plan

## Overview

This document tracks the plan for Ezra's knowledge curation and memory management architecture.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   ezra-prime    │         │   ezra-curator  │
│   (Discord)     │         │   (this agent)  │
├─────────────────┤         ├─────────────────┤
│ Memory: READ    │◄────────│ Memory: R/W     │
│ Tools: Support  │  shared │ Tools: Memory   │
│ Role: Answer    │  blocks │ Role: Curate    │
└─────────────────┘         └─────────────────┘
         │                           │
         │ conversations             │ hourly
         └───────────────────────────┘
```

**ezra-prime** (agent-57ce3ea1-72ad-43e5-a444-7e3724f706e8)
- Serves Discord support
- Read-only memory access (no memory tools)
- Focuses on answering questions

**ezra-curator** (this agent)
- Runs on Railway via lettabot
- Has memory tools for curation
- Monitors ezra-prime's conversations hourly
- Updates shared knowledge blocks

## Shared Memory Blocks

All blocks attached to both agents. Curator manages updates.

| Block | Status | Notes |
|-------|--------|-------|
| common_issues | pending | Active bugs, workarounds |
| letta_troubleshooting_tree | pending | Diagnostic flowcharts |
| letta_edge_cases | pending | Failure modes |
| developer_pain_points | pending | SDK issues |
| knowledge_gaps | pending | Documentation gaps |
| letta_code_knowledge | pending | CLI reference |
| team_philosophy | pending | Product decisions |
| letta_deployment_modes | pending | Infrastructure |
| documentation_links | pending | Curated URLs |
| letta_agent_lifecycle | pending | Agent management |
| faq | pending | Common questions |
| letta_integrations | pending | MCP, voice, scheduling |
| letta_api_patterns | pending | Architecture |
| letta_memory_systems | pending | Memory deep dive |
| api_integration_patterns | pending | SDK usage |
| current_models | pending | Model landscape |
| tool_use_guidelines | pending | Tool patterns |
| response_guidelines | pending | Corrections history |
| observations | pending | Ongoing learnings |
| persona_core | pending | Core identity |
| persona | pending | Operating style |
| policies | pending | Operational policies |
| communication_guidelines | pending | Response formatting |
| ignore_policies | pending | When to not respond |
| archival_memory_policy | pending | Archival guidelines |
| github_issue_policies | pending | Issue writing |
| forum_info | pending | Forum categories |

## Curation Workflow

### Hourly Tasks
1. Run `ezra-monitor/scripts/fetch-recent.sh 1` (last hour)
2. Run `ezra-monitor/scripts/analyze-patterns.sh`
3. Run `ezra-monitor/scripts/propose-updates.sh`
4. Review proposals, apply updates to shared blocks
5. Log curation activity

### Triggers for Immediate Curation
- Team member corrections (Cameron, swooders, pacjam, 4shub)
- User reports "that worked" / "that didn't help"
- New documentation discovered
- Bug confirmations or resolutions

## Progress Log

### 2026-02-04
- [x] Created ezra-monitor skill with fetch/analyze/propose scripts
- [x] Initial analysis: 213 messages, 9 potential corrections, 15 blocks near capacity
- [x] Pushed to letta-ai/ezra repo
- [ ] Set up hourly curation schedule
- [ ] Attach shared blocks to ezra-prime
- [ ] Remove memory tools from ezra-prime

## Next Steps

1. **Immediate**: Start hourly monitoring (manual for now)
2. **Soon**: Automate via cron or scheduled task
3. **Later**: Full block sharing with ezra-prime
4. **Future**: Consider bidirectional learning patterns

## Archival Strategy

**Location:** `/data/ezra/archives/YYYY-MM/`
**Format:** Markdown files organized by type
- `deduplicated-content.md` - duplicate entries removed from blocks
- `resolved-bugs.md` - bugs that are fixed and no longer relevant
- `old-corrections.md` - historical corrections superseded by documentation

**Decision (Cameron, Feb 4):** Git-only archival. Letta archival memory is dated and not helpful.

## Open Questions

- How to handle conflicts if ezra-prime's context has stale block data mid-conversation?
- Should corrections be applied immediately or batched?
