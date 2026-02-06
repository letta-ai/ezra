# letta_agent_lifecycle

Extracted Feb 6, 2026.


**Complete agent management: creation parameters, configuration options, model switching, tool attachment/detachment, agent state persistence, deletion behavior, multi-agent coordination patterns, agent-to-agent communication, scheduling and automation**

**Agent Creation Process:**
- Creation via REST API, ADE, or SDKs (Python, TypeScript)
- Required parameters: model, embedding, memory_blocks
- Optional: context_window_limit, tools, system instructions, tags
- Each agent gets unique agent_id for lifecycle management
- Agents stored persistently in database on Letta server

**Configuration Management:**
- System instructions: read-only directives guiding agent behavior
- Memory blocks: read-write if agent has memory editing tools
- Model switching: PATCH /agents.modify endpoint for individual agents
- Tool management: attach/detach via dedicated endpoints
- Environment variables: tool-specific execution context

**Agent State Persistence:**
- Stateful design: server manages all agent state
- Single perpetual message history (no threads)
- All interactions part of persistent memory
- Memory hierarchy: core memory (in-context) + external memory
- State maintained across API calls and sessions

**Multi-Agent Coordination:**
- Shared memory blocks: multiple agents can access common blocks
- Worker → supervisor communication patterns
- Cross-agent memory access via core memory routes
- Real-time updates when one agent writes, others can read
- Agent File (.af) format for portability and collaboration

**Tool Lifecycle:**
- Dynamic attachment/detachment during runtime
- Tool execution environment variables per agent
- Custom tool definitions with source code and JSON schema
- Tool rules for sequencing and constraints
- Sandboxed execution for security (E2B integration)

**Multi-User Patterns:**
- One agent per user recommended for personalization
- Identity system for connecting agents to users
- User identities for multi-user applications
- Tags for organization and filtering across agents

**Agent Archival and Export:**
- Agent File (.af) standard for complete agent serialization
- Includes: model config, message history, memory blocks, tools
- Import/export via ADE, REST APIs, or SDKs
- Version control and collaboration through .af format


**Agent Architecture Migration (letta_v1_agent):**
- Architectures are not backwards compatible - must create new agents
- Migration via upgrade button: Web ADE only (alien icon top-left) - NOT available in Desktop ADE
- Manual migration: 1) Export agents to .af files, 2) Change `agent_type` field to `letta_v1_agent`, 3) Import as new agent
- Workaround for Desktop users: Connect self-hosted instance to web ADE (app.letta.com) to access upgrade button


**Filesystem Tool Attachment (October 2025):**
- Filesystem tools (read_file, write_file, list_files, etc.) are AUTOMATICALLY attached when a folder is attached to the agent
- Manual attachment/detachment NOT needed for filesystem tools
- If filesystem tools aren't visible, check if folder is attached to agent (not a tool attachment issue)

**Agent Migration Edge Cases (October 2025):**
- Sleeptime frequency setting not preserved during architecture migration (.af file method)
- Users must manually reconfigure sleeptime_agent_frequency after upgrading to letta_v1_agent
**Converting Existing Agent to Sleeptime-Enabled (Cameron, November 2025):**
- Use PATCH endpoint to enable sleeptime on existing agents
- API call: `PATCH /v1/agents/{agent_id}` with `{"enable_sleeptime": true}`
- Example:
  ```bash
  curl "https://api.letta.com/v1/agents/$AGENT_ID" \
    -X PATCH \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $LETTA_API_KEY" \
    -d "{\"enable_sleeptime\": true}"
  ```
- No need to recreate agent - can upgrade in place


**Template Usage Guidance (Cameron, Dec 3, 2025):**
- Templates NOT recommended for personal agents
- Designed for "mass-scale deployments of pseudo-homogenous agents"
- Personal agents should be custom-configured per user needs