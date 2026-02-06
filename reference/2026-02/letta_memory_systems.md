# letta_memory_systems

Extracted Feb 6, 2026.

**Deep dive into MemGPT architecture: core memory blocks (persona, user, custom), archival memory mechanics, context window management, memory persistence patterns, shared memory between agents, memory block CRUD operations, character limits and overflow handling**

**MemGPT Foundation:**
- Letta built by MemGPT creators - inherits core LLM Operating System principles
- Self-editing memory system with memory hierarchy and context window management
- Chat-focused core memory split: agent persona + user information
- Agent can update its own personality and user knowledge over time

**Core Memory Architecture:**
- Always accessible within agent's context window
- Three main types: persona (agent identity), human (user info), custom blocks
- Individually persisted in DB with unique block_id for API access
- Memory blocks = discrete functional units for context management

**Memory Block Structure:**
- Label: identifier for the memory block
- Value: string data content with character limits
- Optional descriptions guiding usage patterns
- Size limits and overflow handling mechanisms
- Block labels are NOT unique - multiple blocks can share the same label
- Agent creation requires block IDs, not labels, because labels aren't unique identifiers
- Use List Blocks API with label_search to find block IDs by label name

**Cross-Agent Memory Patterns:**
- Shared memory blocks: multiple agents can access common blocks
- Memory block inheritance: worker → supervisor agent communication patterns
- API access: agents can read/write other agents' memory blocks via core memory routes
- Real-time updates: when one agent writes, others can immediately read

**Memory Hierarchy:**
- Core Memory: in-context (persona, user, custom blocks)
- External Memory: out-of-context (conversation history, vector databases)
- Persistent storage: all blocks stored in database for agent lifecycle continuity

**Management Operations:**
- Manual control: developers can view/modify memory blocks directly
- Automatic management: agents self-edit based on interactions
- Cross-reference capability: agents can link information across blocks

**Shared Memory Concurrency (October 2025):**
- Locking: Database-level (PostgreSQL row-level locking)
- memory_insert: Most robust for concurrent writes (append operations)
- memory_replace: Can fail in race conditions if target string changes before DB write
- memory_rethink: Last-writer-wins (complete block overwrite, no merge)

**Attaching Memory Blocks in ADE (October 2025):**
- Click "Advanced" in the block viewer for the agent
- Click "Attach block" on the top left
- Find your block
- Click "Attach block" on the top right
- This allows attaching existing blocks to agents without using SDK


**Prompt Caching Behavior (pacjam, Dec 3, 2025):**
- Letta implements proper prompt caching techniques when possible
- Memory block edits invalidate cache for a single turn only
- Cache invalidation is temporary and localized to the turn where memory changes


**Memory Block Label Patterns (Cameron, Dec 9, 2025):**
- Labels can contain "/" characters to mirror filesystem structure
- Useful for organizing hierarchical information (e.g., "docs/api/endpoints")
- Enables shared markdown repo patterns across agents

**Compaction/Summarization Docs (Cameron, Dec 19, 2025):**
- Guide: https://docs.letta.com/guides/agents/compaction/
- Upcoming: Templated variables in system prompts (timezone, agent_id, etc.)

**Memory Tiering & Curation Pattern (Jan 2026):**
- Memory hierarchy as cache tiers: Core memory (hot) → Archival (warm) → External RAG/Filesystem (cold)
- Promotion triggers: Access frequency, successful retrieval, agent decision-making dependency
- Tier transitions:
  - External RAG → Archival: Agent successfully uses content
  - Archival → Core block: Referenced 3+ times in recent conversations
  - Filesystem → Archival: File content cited in decisions
  - Filesystem → Core: Config/reference used every session
- Sleeptime as natural curator: Scans conversation history, promotes based on access patterns, demotes stale content
- Anti-pattern: Auto-promoting everything - value is in curation based on actual use
- Example use cases:
  - Customer support: Database → Recent tickets archival → Active issues core block
  - Research assistant: PDFs filesystem → Key findings archival → Current hypothesis core block
  - Personal assistant: Google Drive RAG → Working docs archival → Preferences/tasks core block