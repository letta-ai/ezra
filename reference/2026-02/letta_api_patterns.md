# letta_api_patterns

Extracted Feb 6, 2026.

**Agent architectures (letta_v1_agent, sleeptime_agent) - ONLY TWO REMAIN (January 2026)**

**CRITICAL UPDATE (Cameron, Jan 27 2026):**
All agent architectures REMOVED except:
1. **letta_v1_agent** (primary)
2. **sleeptime_agent** (background processing)



**Letta V1 Agent (letta_v1_agent) - Primary Architecture:**
- Primary and default architecture
- Deprecated: send_message tool, heartbeats, prompted reasoning tokens
- Native reasoning via Responses API, encrypted reasoning across providers
- Direct assistant message generation (not via tool calls)
- Works with ANY LLM (tool calling no longer required)
- Optimized for GPT-5 and Claude 4.5 Sonnet
- Simpler system prompts (agentic control baked into models)
- Trade-offs: no prompted reasoning for mini models, limited tool rules on AssistantMessage
- Can add custom finish_turn tool if explicit turn termination needed
- archival_memory_insert/search: NOT attached by default (opt-in)

**Sleeptime Agent (sleeptime_agent) - Background Processing:**
- Runs periodic background tasks
- Can be enabled on agents for automated processing
- Important but not directly interacted with

**Default Creation (November 2025):**
- ADE-created agents default to letta_v1_agent
- API may require specifying agent_type
- Team recommends letta_v1_agent for stability and GPT-5/Responses API compatibility

**Message Approval Architecture (Cameron, November 2025):**
- Don't use Modify Message API for customer service approval workflows
- Instead: Custom tool like suggest_response with approval requirements
- Pattern: Agent calls tool → Human approves/denies → Extract reason from return
- Recommended HITL pattern for message-level approval
- send_message tool NOT available on letta_v1_agent

**Memory Tool Compatibility (Cameron, November-December 2025):**
- Optimized for Anthropic models - post-trained on it specifically
- Letta "basically copied" memory tool from Anthropic (Cameron, Nov 15)
- Memory omni tool replaces other memory tools except rethink (Cameron, Dec 8)
- Unique capability: create/delete memory blocks dynamically
- Other models may struggle - OpenAI models "a little less good at it"
- GLM 4.6 "does okay as well" (Cameron, Dec 8)
- Memory tool accepts BOTH formats: /memories/<label> and <label> (intended behavior)
- /memories/ prefix designed to match Claude's post-training set

**Inbox Feature (November 2025):**
- Centralized approval management across all agents
- Available in Letta Labs
- Use case: HITL workflows with multiple autonomous agents
- Cameron: "check if agents have emails to send, code edits to make, etc."


**Sleeptime Chat History Mechanism (Cameron, Dec 3, 2025):**
- Group manager copies most recent N messages into user prompt
- Mechanism: transcript injection via group manager, not shared memory blocks
- Explains how sleeptime agent receives conversation context


**Dynamic Block Attachment for Multi-Character Apps (Dec 17, 2025):**
- Start conversation: attach character block → chat → end: optionally detach
- Trade-off: Keep attached (faster, contextual) vs detach (clean, no accumulation)
- Recommended: Keep 1-3 recent character blocks, detach older
- Relationships in archival with tags, not dependent on block attachment


**Voice Sleeptime Agent Default Tools (Dec 20, 2025):**
- search_memory: Voice-specific search tool auto-attached to letta_voice_sleeptime agents
- Features: Time-windowing (start_minutes_ago, end_minutes_ago), convo_keyword_queries
- Automatically uses latest user message as query (optimized for voice latency)
- Different from standard conversation_search (which requires explicit query string)
- Auto-attached when creating agents from "Start from scratch" in ADE (voice templates)


**Streaming Message Types (v0.16.4+, Feb 2026):**
- stop_reason: Turn termination (end_turn, max_tokens, tool_use, stop_sequence, length)
- usage_statistics: Token metrics (prompt/completion/total/reasoning/cached tokens, step_count, run_ids)
- Appear at end of streaming turns for monitoring/debugging