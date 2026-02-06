# letta_edge_cases

Extracted from core memory Feb 6, 2026.

**Active Edge Cases & Failure Modes (Jan 2026)**

**Letta API-Only Features:**
- `/v1/openai/{agent_id}/chat/completions` - NOT in self-hosted OSS
- Projects feature - Cloud only, use tags for self-hosted isolation
- Templates - Cloud only, use .af files for self-hosted

**Model-Specific Issues:**
- Gemini 3 Pro: "thought_signature" error - use Gemini 2.5 instead
- OpenRouter: Tool calling unreliable (proxy layer issues)
- Ollama: Poor tool calling on smaller models, "big refactor" coming

**Known Limitations:**
- Filesystem does NOT support images - use message attachments
- Video streaming NOT supported (Gemini-only feature)
- Structured output + tool calling incompatible (cannot use both)
- Chat completions endpoint doesn't stream tool calls properly (affects LiveKit)

**Self-Hosted Gotchas:**
- LM Studio Desktop: 30K context cap regardless of model (validation bug)
- LM Studio endpoint types: "lmstudio_openai" deprecated, use "lmstudio"
- SECURE=true blocks frontend - use app.letta.com remote server feature
- Embedding misconfiguration: defaults to Cloud service without auth

**SDK/API Edge Cases:**
- Agent duplication: May cause silent failures in integrations - create fresh instead
- Block label uniqueness: One block per label per agent (UniqueViolationError)
- SDK retry: Each retry = NEW LLM call with full cost
- stream_tokens=True: Tool calls appear as partial JSON chunks

**Performance:**
- Android SSE: OS-level buffering - use WebView workaround
- Context window: Larger = slower + less reliable (32K default recommended)

**Historical edge cases archived Jan 9, 2026 - search archival with tags: edge-cases, archived**

**Filesystem Access Pattern (Jan 23, 2026):**
- Files NOT auto-included in agent context (common misconception)
- Agent workflow: list files → search content → open specific files
- Deliberate vs automatic: Agents explicitly decide what to read (not RAG-style auto-retrieval)
- All file types (PDFs, code, JSON) parsed to text/markdown for agent consumption

**Note Tool Programmatic Bypass (Jan 23, 2026):**
- `/note_directory` block maintained by note tool code, not Letta server
- Direct API calls (POST /v1/blocks) bypass note tool's directory update logic
- Workaround: Trigger note tool once to create directory, then manually update if needed
- Template behavior: Agents get snapshot at creation time, future template changes don't propagate


**Desktop ADE Closed Source (Jan 24, 2026):**
- Desktop ADE source code is NOT publicly available (never was public)
- Closed-source Electron application (not at github.com/letta-ai/letta/tree/main/desktop)
- Settings persistence bugs known issue (context window reverts to hardcoded 30k default)
- Root cause: Desktop ADE sends PATCH requests with 30k hardcoded value on every interaction
- Embedded server mode deprecated and will be removed
- Workaround: Use Web ADE for reliable configuration management, or server-side patches


**Tags Not Working in v0.16.2 (Jan 29, 2026):**
- Issue: Tags parameter accepted but values not stored/returned
- Root cause: Incomplete tags implementation in v0.16.2
- Symptom: agent.tags is not None, but list is empty or missing values
- Workarounds: Upgrade to latest server, use HTTP identities endpoint, or name prefixes
- Cameron recommended tags migration, but feature incomplete in older versions

**Tags Not Working in v0.16.2-0.16.4 (Jan 29, 2026):**
- Issue: Tags parameter accepted but values not stored/returned
- Root cause: Incomplete tags implementation in v0.16.2-0.16.4
- Symptom: agent.tags is not None, but list is empty or missing values
- Workarounds: Upgrade to latest server, use HTTP identities endpoint, or name prefixes
- Cameron recommended tags migration, but feature incomplete in older versions
- **CRITICAL:** Self-hosted only - Letta Cloud tags work correctly (tested Jan 29)


**Version Downgrade Database Pollution (Jan 30, 2026, fimeg):**
- Symptom: "Tool call incomplete - missing name or arguments" errors after downgrading letta-code
- Root cause: Stale tool definitions or MCP server registrations from newer version in database
- Tool DOES execute but structure broken - not model hallucination
- Affected: letta-code version cycling (0.13.6+ → 0.13.11 → downgrade)
- Solutions: Clean database, detach suspicious tools, or create fresh agent to test
- Pattern: Database schema mismatches persist across version downgrades


**OpenWebUI Integration Limitation (Jan 31, 2026, kyujaq):**
- OpenWebUI doesn't accept Letta's OpenAI-compatible endpoint URL format
- Letta endpoint structure: `https://api.letta.com/v1/openai/{agent_id}/chat/completions`
- OpenWebUI expects: base URL ending at `/v1` (OpenAI standard)
- URL validation rejects anything after `/v1`
- Workarounds: 
  1. Reverse proxy to rewrite URLs
  2. Try putting agent ID in model field (may not work)
  3. Use standard Letta ADE/SDK instead
- Root cause: OpenWebUI validates OpenAI-standard URL structure, incompatible with Letta's agent-scoped endpoints


**Cross-User Agent Messaging Limitation (Jan 31, 2026, antibearo):**
- Cannot send messages from User A's agent to User B's agent across different orgs
- 429 errors = authorization failure (API keys scoped to organizations)
- Built-in messaging tools only work within same API key/organization scope
- Solutions: same organization + RBAC, relay backend, client-side tokens
- Architectural security limitation by design


**MCP Local Server Support Limitation (Feb 1, 2026, mathegeek):**
- Cannot use letta-code + Letta Cloud with local MCP servers
- Letta Cloud only supports Streamable HTTP (requires publicly accessible URL)
- stdio transport (for local servers) is self-hosted only
- Documentation: "stdio is Docker only. The Letta API does not support stdio."
- letta-code doesn't proxy MCP connections (unlike filesystem tools)
- Workarounds: 
  1. Use self-hosted Letta (Docker) which supports stdio
  2. Expose local MCP publicly (ngrok, etc.)
  3. Use MCP via streamable HTTP to host.docker.internal (self-hosted)
- Root cause: MCP servers must be registered in Letta server config, server makes HTTP requests directly
- Pattern: Filesystem tools work (client-side), MCP doesn't (server-side)


**Windows letta-code Bash Tool PATH Bug - DIAGNOSED (Feb 2, 2026, mathegeek):**
- **Root cause found:** shellEnv.ts lines 54-56 - case-sensitive PATH access
- Windows uses `env.Path`, code reads/writes `env.PATH` → creates empty PATH variable
- Destructuring `{ ...process.env }` loses Windows case-insensitive handling
- **Fix:** Find actual PATH key case-insensitively, use same key for read and write
- **GitHub:** https://github.com/letta-ai/letta-code/issues/783
- **Impact:** ALL Windows users - Bash tool can't find executables
- **Workaround until fix:** Full paths only (C:\\Program Files\\nodejs\\node.exe)
- Charles notified, fix should unblock all Windows devs once merged


**Z.ai/GLM Streaming Not Supported (Feb 4, 2026):**
- Z.ai provider doesn't support streaming in Letta
- Error: "Streaming not supported for provider zai"
- Solution: Use non-streaming endpoint or switch providers

**Sleeptime ADE Bug - Silent Failure (Feb 4, 2026, cryingsurrogate):**
- Self-hosted: "Enable Sleeptime" button fails silently when embedding_config is null
- UI thinks it worked but no sleeptime agent created
- managed_group returns null
- Related to OpenRouter/embedding config issues

**Google Drive "My Drive" Space Handling (Feb 2, 2026, dean051537):**
- Issue: Cannot access Google Drive mounted at "G:\My Drive" due to space in path
- Affects: Windows users with Google Drive Desktop app
- Workarounds:
  1. Junction: `mklink /J C:\gdrive "G:\My Drive"` (must use full command with quotes)
  2. Folder ID: Use Drive folder ID instead of path
  3. Subst: `subst M: "G:\My Drive"` to map to drive letter
  4. Direct path with escaping: `"G:\\My Drive\\file.txt"` in Python
- Common mistake: Incomplete mklink command missing closing quote/path


**Sleeptime Group Architecture - Correct Pattern (Feb 6, 2026):**
- Primary agent (Ani) = `manager_agent_id` in groups table
- Primary agent has `multi_agent_group_id` = its own group ID
- Sleeptime agent (Aster) listed in `agent_ids` JSON array in groups table
- Execution flow: User message → Ani processes → Ani finishes → SleeptimeMultiAgentV4 runs Aster
- `agent_state.multi_agent_group` finds groups where agent is manager (NOT member)
- Log warning "multi_agent_group is None" means `multi_agent_group_id` not set on primary agent
- Common mistake: Thinking curator should be manager (WRONG - primary is manager)



**Sleeptime Tool Execution (Feb 6, fimeg clarification):**
- Sleeptime does NOT re-execute primary's tool calls
- Sleeptime receives TRANSCRIPT of tool calls + results (already executed)
- Reviews what happened, extracts learnings, updates memory blocks