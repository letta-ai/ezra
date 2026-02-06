# letta_deployment_modes

Extracted Feb 6, 2026.

**Infrastructure and deployment: Letta Cloud vs self-hosted comparison, Docker configuration, database setup (PostgreSQL), environment variables, scaling considerations, networking, security, backup/restore procedures**

**Deployment Architecture:**
- Letta Cloud: managed service with rapid updates
- Self-hosted: PostgreSQL database + FastAPI API server
- Docker recommended for self-hosted deployments
- Web ADE (app.letta.com): Can connect to both Cloud and self-hosted servers via "Add remote server"
- Desktop ADE: Connects to both Cloud and self-hosted servers (PostgreSQL only - SQLite removed)
- Custom UI: Build via SDK/API

**Docker Configuration:**
```bash
docker run \
  -v ~/.letta/.persist/pgdata:/var/lib/postgresql/data \
  -p 8283:8283 \
  -p 5432:5432 \
  -e OPENAI_API_KEY="your_key" \
  -e ANTHROPIC_API_KEY="your_key" \
  -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  letta/letta:latest
```

**Database Setup (PostgreSQL):**
- Default credentials: user/password/db all = `letta`
- Required extension: `pgvector` for vector operations
- Custom DB: Set `LETTA_PG_URI` environment variable
- Port 5432 for direct database access via pgAdmin

**Performance Tuning:**
- `LETTA_UVICORN_WORKERS`: Worker process count (default varies)
- `LETTA_PG_POOL_SIZE`: Concurrent connections (default: 80)
- `LETTA_PG_MAX_OVERFLOW`: Maximum overflow (default: 30)
- `LETTA_PG_POOL_TIMEOUT`: Connection wait time (default: 30s)
- `LETTA_PG_POOL_RECYCLE`: Connection recycling (default: 1800s)

**Security Configuration:**
- Production: Enable `SECURE=true` and `LETTA_SERVER_PASSWORD`
- Default development runs without authentication
- API keys via environment variables or .env file

**Letta API vs Docker (Terminology Jan 2026):**
- "Letta Cloud" DEPRECATED → Use "Letta API" (service) or "Letta Platform" (console/ADE)
- "Self-hosted server" → "Docker" or "Letta server running in Docker"
- "Self-hosted" now refers to agent execution environment (e.g., "self-hosted Letta Code")
- Letta API: ~2s latency, rapid updates, managed
- Docker: ~600ms latency, version lag, manual management

**Remote Server Connection:**
- ADE "Add remote server" for external deployments
- Supports EC2, other cloud providers
- Requires server IP and password (if configured)

**Embedding Provider Updates (October 2025):**
- LM Studio and Ollama now offer embeddings
- Enables fully local deployments without external embedding API dependencies


**Templates (Cameron, Dec 3, 2025):**
- Cloud-only feature, will remain that way
- Built for massive scale deployments
- Self-hosted alternative: use Agent Files (.af) but requires more manual work


**BYOK Grandfathering (Cameron, Dec 4, 2025):**
- Existing BYOK users likely grandfathered in despite enterprise-only policy
- Example: taurean (void/void-2) continuing to use BYOK


**letta-code OAuth (Cameron, vedant_0200, Dec 9 2025):**
- OAuth flow launches if starting letta-code without API key
- OAuth is to Letta (not Claude Code, Codex, or other external subscriptions)
- Cannot use Claude Code or similar subscription keys with letta-code
- No current integrations to connect Letta features to external subscriptions

**letta-code BYOK (Cameron, Dec 19 2025):**
- BYOK now available on Pro plan
- Settings: https://app.letta.com/settings/organization/models
- Use case: cost centralization (user controls provider billing separate from Letta billing)

**Redis Benefits (Cameron, Dec 23 2025):**
- Background streaming (fire-and-forget calls without holding connections)
- Token count caching (Anthropic/Gemini APIs)
- Embedding caching for passages
- User lookup caching
- Run cancellation support
- Most impactful for production: background streaming


**xAI/Grok Model Support (January 2026):**
- Letta Cloud: Grok models not available (curated model list, xAI not yet added)
- Self-hosted: Can use Grok via OpenAI-compatible endpoint
- Configuration: XAI_API_KEY env var, model_endpoint="https://api.x.ai/v1"
- Model format: "openai/grok-3" with model_endpoint_type="openai"


**AWS Bedrock-Only Deployment (Feb 2, 2026):**
- Enterprise requirement: All data within AWS infrastructure
- IAM role with Bedrock permissions on EC2 (no hardcoded keys)
- Environment variables: AWS_REGION, LETTA_LLM_ENDPOINT_TYPE="bedrock"
- Disable Cloud models: Database-level or environment config
- Ensures: No external API calls, only AWS Bedrock models available