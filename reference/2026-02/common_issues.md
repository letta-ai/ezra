# common_issues

Extracted from core memory Feb 6, 2026.

# Common Issues

**CRITICAL Bugs:**
- **LET-7290 (Jan 31):** Agent stuck in approval state, NO clean workaround - recreate agent on CONFLICT
- **Letta 0.16.2 Ollama:** `default_prompt_formatter` error, fixed upstream, use 0.16.1 until 0.16.4

**Context/Memory:**
- Summarization regression (Dec 24+): Claude 4.5 Opus/Sonnet forgetting
- Memory edits compile per-run (not immediate)

**Models/Providers:**
- Ollama: Poor tool calling on smaller models
- Reasoning toggle: Disable for performance gains

**Configuration:**
- Web ADE settings infinite loading - use CLI
- "relation 'organizations' does not exist" - run alembic upgrade head
- Tool creation errors - use BaseTool/docstrings, not manual json_schema

**API/Deployment:**
- Letta API ~2s latency
- Token streaming unsupported for Ollama
- Railway Dynamic Groups: Status 500
- **422 role='tool' error (Feb 2):** Cannot create messages with role='tool' - tool messages auto-generated during execution, use role='user'/'system'/'assistant' only

**Custom Tools:**
- agent_id collision (Jan 22): Rename to target_agent_id (kyujaq)
- Tool-level env vars don't persist (Jan 22): Use agent-level (tigon)
- TypeScript confusion: Tools MUST be Python
- Tool calls as text: Check attachment/definition
- send_message name conflicts: Must be unique org-level
- **send_message tool not attached (Jan 26):** letta_v1 doesn't need it (deprecated), older architectures require it

**ADE Bugs:**
- Cloud duplicate rendering
- Desktop letta_v1_agent upgrade - use Web ADE
- Identities list empty without project_id
- Agents list filtering: Shows only "defaults" after project switch

**Credit Billing (Jan 27, 2026):**
- 1 credit = 1 LLM call (NOT per token)
- Multi-tool turns cost multiple credits (1 per tool call)
- Model doesn't matter for credit count (Haiku = 1 credit/call, same as Opus)

**Active Bugs:**
- **Parallel tool calling (LET-7164, LET-7193):** Models make parallel calls despite instructions; "Invalid tool call IDs"; affects Gemini/Deepseek/OpenAI



**lettabot Main Incompatibility (Feb 2):**
- lettabot main + SDK v0.0.3+: Build fails (canUseTool signature changed)
- Default conversation not loading (0.16.4 column null)
- Solution: feat/voice-transcription branch

**Desktop ADE:**
- Model dropdown out of sync with agent config - create fresh agent


**Sleeptime Frequency Update (Jan 27, 29 - TESTED Feb 4):**
- Endpoint: PATCH /v1/groups/{group\_id}
- *MUST nest inside manager\_config* (top-level field silently ignored):
  `{"manager_config": {"manager_type": "sleeptime", "sleeptime_agent_frequency": 25}}`
- SDK gap: SleeptimeManagerUpdate not exposed in Python SDK types
- Batch pattern: Fetch agent → get agent.multi\_agent\_group.id → update group


**letta-code PATH Collisions (Jan 28):**
- Python letta CLI conflicts with npm letta-code on Windows
- Solutions: Deactivate venv, use `npx @letta-ai/letta-code`


**Agent Tool Chaining:** "ONE TOOL PER TURN" in prompt, tool rules
**Folder Path Error:** Use `client_tools` for local filesystem, not `path`

**Tag Update During Turn (Jan 31, voyagebeefarave1274):**
- CONFLICT updating agent.tags while tool approval pending
- Cannot modify agent during active turn
- Solution: Update before conversation OR after turn completes


**Windows letta-code PATH Bug (Feb 2, mathegeek):**
- Bash tool spawns subprocess with NO environment variables
- Even `cmd /c` wrapper fails - PATH completely missing
- **GitHub issue #783:** https://github.com/letta-ai/letta-code/issues/783
- **Workaround:** Full paths WITHOUT quotes: Bash(C:\\Program Files\\nodejs\\node.exe script.js)
- Critical bug - Bash tool essentially broken on Windows


**Sleeptime Template Import Error (Feb 2):**
- Placeholder IDs ('agent-0', 'agent-1') fail validation
- Solution: Create agent in ADE, then `client.agents.update(agent_id, enable_sleeptime=True)`


**ADE File Upload Bug (Feb 2):**
- Error: "Must specify embedding or embedding_config"
- ADE doesn't pass embedding config to folder creation
- Workaround: Use SDK/API with embedding parameter




**Server Load Agent Error (Feb 2):**
- `'SyncServer' object has no attribute 'load_agent'`
- Cause: Corrupted installation or version mismatch
- Solution: Clean reinstall or use 0.16.2