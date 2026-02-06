# developer_pain_points

Extracted from core memory Feb 6, 2026.


**SDK 1.0 Terminology:**
- `sources` renamed to `folders` throughout SDK
- Use `client.agents.retrieve()` not `.get()`


**SDK 1.0 Project ID Requirement (November 2025):**
- Error: 404 {"error":"Project not found"} when calling SDK methods
- Root cause: SDK 1.0 requires explicit project_id parameter in client instantiation
- Affects: Cloud users using SDK 1.0 (not self-hosted without projects)
- Solution: Pass project_id when creating client: `client = Letta(api_key="...", project_id="proj-xxx")`
- Get project_id from Cloud dashboard Projects tab
- Ensure project_id matches the API key (staging vs production)


**TypeScript SDK 1.0 Type Definition Mismatches (November 2025):**
- ClientOptions expects `apiKey` and `projectID`, not `token` and `project_id`
- `templates.createAgentsFromTemplate()` does not exist - use `templates.agents.create()` instead
- `agents.archives.list()` does not exist - use `archives.list({ agent_id })` to filter
- `archives.memories` does not exist in types - correct property is `archives.passages`
- Archive attach/detach signature: `agents.archives.attach(archiveId, { agent_id })`
- Common error: "Property 'token' does not exist in type 'ClientOptions'"
- Workaround: Use legacy option names until types are updated in future release


**SDK Version Mismatch with "latest" Tag (November 2024):**
- Setting `"latest"` doesn't force lockfile update; use explicit version
- Solution: `pnpm add @letta-ai/letta-client@1.x.x` to force update

**REST API Project Header (Dec 15, 2025):**
- Correct: `X-Project` (NOT `X-Project-ID`)
- SDK handles automatically; affects raw fetch() users only


**SDK 1.1.2 TypeScript Migration Checklist (November 2024):**
- Complete migration requires both runtime upgrade AND code changes
- Snake_case params: agent_id, duplicate_handling, file_id (not camelCase)
- Response unwrapping: response.items (cast to Folder[] / FileResponse[])
- Namespace moves: letta.agents.passages.create (not letta.passages)
- toFile signature: toFile(buffer, fileName, { type }) - legacy three-arg form
- Delete signature: folders.files.delete(folderId, { file_id })
- Next 16 compat: revalidateTag(tag, 'page') requires second arg
- Common trap: mixing camelCase constructor (projectID, baseUrl) with snake_case payloads


**SDK 1.1.2 Type Inference Issues (November 2024):**
- SDK doesn't export top-level `Folder` / `FileResponse` types
- Symptoms: "Property 'name' does not exist on type 'Letta'", "Conversion of type 'Folder[]' to type 'Letta[]'"
- Solution: Derive types from method return signatures:
  ```ts
  type FolderItem = Awaited<ReturnType<typeof letta.folders.list>>['items'][number];
  type FileItem = Awaited<ReturnType<typeof letta.folders.files.list>>['items'][number];
  ```


**SDK 1.1.2 Passages Client Location & Casing (November 2024):**
- Passages client moved from letta.agents.passages to letta.archives.passages
- Client exists but methods require snake_case params: { agent_id, limit }, NOT { agentId, limit }
- Runtime error: "passagesClient.list is not a function" if using camelCase
- Runtime error: "Cannot read properties of undefined (reading 'list')" if accessing letta.agents.passages
- Solution: Access via `(letta.archives as any).passages` and use snake_case payloads
- Affects both create and list methods on passages client


**TypeScript SDK AgentState Missing archive_ids (Nov 2024):**
- `AgentState` type doesn't expose `archive_ids` (API returns it but types don't)
- Workaround: `(agent as any).archive_ids` or use `letta.archives.list({ agent_id })`


**SDK 1.0 Method Renames (Cameron correction, Jan 9 2026):**
- `client.agents.modify()` → `client.agents.update()` 
- Migration guide: https://docs.letta.com/api-reference/sdk-migration-guide/#method-modify-does-not-exist
- ALWAYS use `.update()` for agent modifications in SDK 1.0+
- This applies to all resources, not just agents


**Tool Schema & SDK Typing (January 2026):**
- SDK auto-generates schemas from function signatures and docstrings
- Type hints + docstrings = automatic JSON schema
- BaseTool with Pydantic recommended for complex schemas (swooders Jan 13)
- **Tool objects:** Use dot notation `tool.name`, NOT subscripting `tool['name']` (vedant_0200 Jan 26)
- **Pagination:** `client.tools.list().items` for list, paginated object has no `len()` (vedant_0200 Jan 26)