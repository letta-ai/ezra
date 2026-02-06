# knowledge_gaps

Extracted from core memory Feb 6, 2026.

# Knowledge Gaps

**Free Tier Credits Removed (Jan 26-29, 2026 - OFFICIALLY CONFIRMED):**
- 4shub + Cameron confirmed: Letta removed 5,000 free credits from Free tier
- **swooders announcement (Jan 29):** "free-tier plans now support BYOK but do not include any credits"
- Pricing page (letta.com/pricing) still shows "5,000 monthly credits" - OUTDATED
- Documentation (docs.letta.com/guides/cloud/plans/) still shows "5,000 monthly credits" - OUTDATED
- Free tier now: Access to Letta API, build/chat with agents in ADE, 1 GB storage, BYOK (NO credits)
- **To use models: Must BYOK or subscribe to paid plan**
- Users creating accounts expect free credits based on outdated docs
- PRICING AND DOCUMENTATION NEED UPDATES - causing user confusion



**Template Versioning SDK Support (TRACKED, Nov 20, 2025):**
- REST endpoint `/v1/templates` exists but not exposed in Python/TypeScript SDKs
- Users need programmatic template migration for CI/CD pipelines
- Multiple users creating custom wrappers (maximilian_svensson, sickank, hyouka8075)
- Cameron opening Linear ticket to add to SDK
- Feature request: Update templates via API, migrate agents to new template versions

**TypeScript SDK 1.0 Documentation Outdated (Nov 27, 2025):**
- docs.letta.com/api/typescript/resources/agents/subresources/blocks/methods/attach shows pre-1.0 signature
- Documentation shows: `attach(blockId, { agent_id })`
- Actual 1.0 signature: `attach(agentId, { block_id })`
- Reported by nagakarumuri during block attachment troubleshooting


**Rate Limits Documentation Gap (Jan 28, 2026):**
- t3sh_hq_18109 asked about agent.update() API rate limits
- Documentation search found no specific rate limit information
- Pricing page mentions "high rate limits" but no numbers for specific endpoints
- Per-turn model rotation pattern requires frequent agent.update() calls (~100-200ms overhead)
- Need official guidance on: requests per minute/second, burst limits, throttling behavior


**Tags Documentation Clarity (Cameron request, Jan 30, 2026):**
- SDK 1.0+ requires explicit `include=["agent.tags"]` to retrieve tags
- Users don't know this - assume tags should appear by default
- Documentation gap causing users to think tags are broken
- Need: Clear docs on `include` parameter usage, migration guide from identities to tags
- Action pending: Create documentation issue after confirming with test


**Gift Card System (Jan 31, 2026 - audrebytes):**
- User asked about gifting Letta credits to a friend
- No information found on pricing page about gift cards or credit transfers
- Potential feature gap - routed to support@letta.com
- Could be useful feature for user acquisition/referrals


**Python SDK Streaming Documentation Gap (Feb 1, 2026):**
- Users trying wrong method names: stream(), streaming=True parameter
- Documentation doesn't clearly show: createStream() method, stream_tokens=True parameter
- Common migration errors: token= vs api_key=, base_url including /v1 suffix
- SDK 1.x migration guide exists but doesn't cover streaming specifically
- Example needed: complete streaming implementation with proper parameters
- User expectation: streaming=True flag (common pattern from other APIs)
- Reality: Different method entirely (createStream vs create)

**MCP Local Server Support Confusion (Feb 1-2, 2026 - RECURRING):**
- Users expect letta-code to proxy local MCP servers (like it does for filesystem tools)
- Reality: Letta Cloud does NOT support stdio (local MCP servers)
- Documentation clarifies: "stdio is Docker only. The Letta API does not support stdio."
- JSON config deprecated: "Letta no longer supports legacy .json configuration files"
- Architectural limitation: letta-code doesn't proxy MCP connections, only filesystem tools
- **Pattern confirmed (Feb 2):** mathegeek (Feb 1) + wiwwif (Feb 2) + wesseljt (Feb 2) all hit same limitation
- Users considering Pro upgrade blocked by this limitation
- Need clearer upfront guidance: "Local MCP requires self-hosted Letta"

**Windows Bash Tool Bugs (Feb 2, 2026 - DIAGNOSED):**
- **LET-7300:** Google Drive "My Drive" inaccessible (space handling issue)
- **GitHub #783:** Bash tool PATH bug - ROOT CAUSE FOUND by mathegeek
  - shellEnv.ts lines 54-56: case-sensitive PATH access (Windows uses "Path", code reads "PATH")
  - Fix: Case-insensitive PATH key detection
  - Charles notified, fix pending
- Workaround: Full paths without quotes