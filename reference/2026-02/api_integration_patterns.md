# api_integration_patterns

Extracted Feb 6, 2026.

**SDK Architecture:**
- Python SDK 1.0: `pip install letta-client` (stable release, November 19 2025)
- **CRITICAL:** Import as `from letta_client import Letta` (NOT `from letta import Letta`)
- TypeScript SDK 1.0: `npm install @letta-ai/letta-client` (stable release, November 19 2025)
- Documentation: https://docs.letta.com/api-reference/sdk-migration-guide (migration)
- All interfaces (ADE, REST API, SDKs) use same underlying API

**Authentication Flows:**
- Letta Cloud: requires `api_key` parameter only (projects deprecated Jan 2026)
- API keys now mapped directly to projects - no `project_id` parameter needed
- Client instantiation: `client = Letta(api_key="LETTA_API_KEY")`
- SDK 1.0 uses `api_key`, NOT `token` (pre-1.0 used `token`)
- Local server: direct connection without api_key (alpha.v19+ allows empty string)

**Core Endpoint Patterns:**
- Stateful API design: server manages agent state, memory, message history
- Agent messaging: `POST /agents/{agent_id}/messages`
- Agent creation: `client.agents.create()` with model, embedding, memory_blocks
- Core memory routes: for cross-agent memory block access
- Batch endpoints: multiple LLM requests in single API call for cost efficiency

**API Response Patterns:**
- Agent responses include: reasoning steps, tool calls, assistant messages
- Message model includes `sender_id` parameter for multi-user scenarios
- Server-Sent Events (SSE) for streaming: `/v1/agent/messages/stream`
- "POST SSE stream started" messages are normal system indicators

**State Management:**
- Stateful server-side: unlike ChatCompletions API which is stateless
- Server handles: agent memory, user personalization, message history
- Individual agents run as services behind REST APIs
- Persistent agent state across API calls and sessions

**Recent API Evolution:**
- SDK 1.0 release (November 2025) - major stable release
- Projects endpoint, batch APIs, reasoning_effort field
- **DEPRECATED (Dec 19):** llm_config in agent creation - use model handles instead (e.g., "openai/gpt-4o")
- List Agent Groups API for multi-agent group management

**Letta as Agent Backend (Pacjam, November 2025):**
- Mental model: "Hosted Claude Code/Agents SDK"
- Common architecture: Letta + application backend (e.g., Letta + Convex)
- Simple use cases: Can use Letta + frontend directly (Letta has client-side access tokens)
- Complex use cases: Application backend stores UI state, Letta handles agent logic
- Example: Next.js → Convex for chat UI/history, Convex → Letta for agent interactions

**When to use Letta vs ChatCompletions:**
- Short sequences (1-3 calls, no retention): ChatCompletions in app backend
- Long-running agents (hours, many tool calls): Use Letta/dedicated agent service
- Long-running agent logic inside main app = durability disaster


**Common API Security Mistakes (November 2025):**
- Relying on client-provided IDs (agent_id, user_id) without cryptographic proof
- Using POST methods for read operations (breaks HTTP semantics, prevents caching)
- Configuring CORS for server-to-server calls (Letta Cloud has no Origin header)
- Missing bearer token requirements in public-facing APIs
- Pattern: Always require Authorization header FIRST, then validate ID mappings


**Next.js Singleton Pattern (Best Practice, Dec 2025):**
```ts
// lib/letta.ts - singleton client
import { LettaClient } from '@letta-ai/letta-client';

export const letta = new LettaClient({
  baseUrl: process.env.LETTA_BASE_URL || 'https://api.letta.com',
  apiKey: process.env.LETTA_API_KEY!,
  projectId: process.env.LETTA_PROJECT_ID,
});

// app/api/send-message/route.ts
import { letta } from '@/lib/letta';
```
- API key stays server-side in env vars
- Single client instance reused across all routes
- Add auth middleware to protect routes


**SDK 1.0 Message & Conversation Patterns (Dec 2025-Jan 2026):**
- SDK expects typed objects: `from letta_client.types import MessageCreateParam`
- Conversations API (TypeScript): `letta.conversations.create({ agent_id, label, summary })`, then `letta.conversations.messages.create(conversation_id, { messages: [...] })`
- Streaming: `letta.conversations.messages.createStream()` with async iteration
- Multimodal: Anthropic format with `type: "image"` and `source: { type: "url", url: "..." }`