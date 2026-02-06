# letta_integrations

Extracted Feb 6, 2026.

**External system connections: custom tool creation, MCP protocol implementation, database connectors, file system integration, scheduling systems (cron, Zapier), webhook patterns, third-party API integrations**

**MCP (Model Context Protocol) Integration:**
- Streamable HTTP: Production-ready, OAuth 2.1, Bearer auth
- stdio: Self-hosted only
- Agent-scoped variables, custom headers
- **Session limitation:** Stateless (LET-7263); workaround: server-side sessions via x-agent-id header

**MCP Server Connection Patterns:**
- ADE: Tool Manager → Add MCP Server (web interface)
- API/SDK: Programmatic integration via letta_client
- Automatic `x-agent-id` header inclusion in HTTP requests
- Tool attachment to agents after server connection
- Supports both local (`npx` servers) and remote deployments

**External Data Sources:**
- File system integration for document processing
- Database connectors via MCP protocol
- Vector database connections for archival memory
- API integrations through custom tools and MCP servers

**Scheduling and Automation:**
- System cron jobs for scheduled agent interactions
- Zapier integration available: https://zapier.com/apps/letta/integrations
- Sleep-time agents for automated processing tasks
- External cron jobs calling Letta Cloud API for 24-hour scheduling

**Custom Tool Development:**
- BaseTool class for Python tool development
- Source code approach with automatic schema generation
- Environment variables for tool execution context
- Sandboxed execution via E2B integration for security
- Tool rules for sequencing and constraint management

**Third-Party System Integration:**
- REST API and SDKs (Python, TypeScript) for application integration
- Agent File (.af) format for portability between systems
- Multi-user identity systems for connecting agents to external user databases
- Webhook patterns through custom tool implementations

**Voice Agent Integration (Team Recommendation, Dec 2025):**
- Voice is "extremely hard to do well" - not Letta's core competency (Cameron, Dec 4)
- **Recommended architecture: Voice + Letta Sidecar Pattern**
  - Voice agent handles real-time conversation (latency-optimized)
  - Letta agent as sidecar for memory/state
  - Sync: Download blocks before prompt, feed messages back after
- Voice platforms: LiveKit and VAPI (docs: https://docs.letta.com/guides/voice/overview/)


**Agent Secrets Scope (November 2025):**
- Agent secrets are agent-level (shared across all users), not per-user
- Cannot pass different auth tokens per user via environment variables
- Use cases: shared API keys, service credentials, base URLs
- Per-user auth: store tokens in DB, inject at request time via proxy or custom tool


**HTTP Request Origin (November 2025):**
- Letta Cloud: Requests originate from Letta's server infrastructure (server-to-server)
- No fixed domain, IP list, or Origin header for CORS allowlisting
- Self-hosted: Requests come from user's deployment environment
- Recommendation: Authenticate via service tokens/signed headers, not domain-based CORS rules


**Cloudseeding - Bluesky Agent Bridge (Community Tool, Dec 2025):**
- Deno-based bridge between Bluesky and Letta agents
- Repository: https://tangled.org/taurean.bryant.land/cloudseeding/
- Created by Taurean Bryant
- Features: dynamic notification checking, full social actions, sleep/wake cycles, reflection sessions, AI transparency declarations
- Quickstart: `deno task config`, edit .env, `deno task mount`, `deno task start`
- Used by void and void-2 social agents on Bluesky
- Production-ready deployment framework for social agents


**Letta Code Sub-Agent Support (Cameron, Dec 18, 2025):**
- Subagents work great now - Cameron off Claude Code entirely


**Perplexity MCP Server (December 2025):**
- Repository: https://github.com/perplexityai/modelcontextprotocol
- Transport: stdio only (not compatible with Letta Cloud)
- Command: `npx -y @perplexity-ai/mcp-server`
- Requires: PERPLEXITY_API_KEY environment variable
- Tools: perplexity_search, perplexity_ask, perplexity_research, perplexity_reason
- Self-hosted only - Cloud workaround requires custom HTTP wrapper or bridge