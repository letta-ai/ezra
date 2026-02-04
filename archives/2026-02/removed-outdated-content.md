# Removed Outdated Content - Feb 4, 2026

## From developer_pain_points - Sources->Folders Migration
```
**Sources → Folders Terminology Change (November 2025):**
- BREAKING CHANGE: `client.sources.*` deprecated - use `client.folders.*` instead
- API endpoint `/v1/sources/` deprecated - use `/v1/folders/`
- Methods renamed: `sources.create` → `folders.create`, `sources.upload_file` → `folders.upload_file`
- Agent methods: `attach_source` → `attach_folder`, `agents.folders.attach()` for SDK 1.0
- All "sources" references no longer relevant - terminology is now "folders" throughout SDK
- Cameron confirmed (Nov 21, 2025): "Any references to sources is no longer relevant"
- Agent retrieval: Use `client.agents.retrieve(agent_id)` not `client.agents.get(agent_id)` in SDK 1.0
```

## From common_issues - Old letta-code versions
```
**letta-code Compatibility:**
- **0.13.6+ (LET-7252):** tool_return schema mismatch - string vs ContentPart[] array
- Workaround: Downgrade to 0.13.5 until 0.16.4 released
- 0.13.11 + 0.16.2: Calls missing `/v1/messages/{id}` endpoint
```

## From letta_api_patterns - Deprecated architectures list
```
**DEPRECATED/REMOVED architectures (will soon no longer be available):**
- memgpt_agent (being removed)
- memgpt_v2_agent (being removed)
- react_agent (being removed)
- workflow_agent (being removed)
- split_thread_agent (being removed)
- voice_convo_agent (being removed)
- voice_sleeptime_agent (being removed)
```
