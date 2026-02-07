---
name: verify-claims
description: Verify factual claims before adding them to agent memory blocks. Use this skill when proposing FAQ entries, documentation updates, or any factual statements about Letta features, APIs, or behavior. Prevents confident-but-wrong assertions.
---

# Verify Claims

Test assumptions against code, docs, and live APIs before committing them to memory.

## When to Use

- Before adding FAQ entries to agent memory
- Before stating "X works like Y" in support responses
- When updating knowledge blocks with new information
- Any time you're about to assert something you haven't directly verified

## Verification Methods

### 1. Code Inspection
Search relevant repos for implementation evidence:
```bash
./scripts/check-code.sh "lettabot supports skills" ~/lettabot
```

### 2. Documentation Search
Search docs.letta.com for official statements:
```bash
./scripts/check-docs.sh "archival memory vector database"
```

### 3. Live API Test
Run actual API calls to verify behavior:
```bash
./scripts/check-api.sh "agents list pagination"
```

### 4. Full Verification (all methods)
```bash
./scripts/verify.sh "claim to verify" [optional: repo_path]
```

## Output Format

Each script outputs:
```
CLAIM: <the claim being tested>
METHOD: <code|docs|api>
STATUS: VERIFIED | NOT_VERIFIED | PARTIAL | NEEDS_MANUAL
EVIDENCE: <what was found>
CONFIDENCE: <high|medium|low>
```

## Workflow

1. **Before adding to memory:** Run verification
2. **If VERIFIED:** Add claim with evidence citation
3. **If NOT_VERIFIED:** Do not add, or add with caveat
4. **If PARTIAL:** Note what's confirmed vs assumed

## Key Repos to Search

- `~/lettabot` - LettaBot implementation
- `~/letta/letta-sdk-api-docs` - SDK documentation
- `~/letta/skills` - Shared skills repo

## Example Session

```bash
# Verify before adding FAQ entry
./scripts/verify.sh "lettabot supports skills"

# Output:
# CLAIM: lettabot supports skills
# STATUS: VERIFIED
# EVIDENCE: 
#   - CODE: installSkillsToAgent in bot.ts
#   - CODE: skills memory block in system-prompt.ts
# CONFIDENCE: high
```

Then add to FAQ with citation: "Lettabot supports skills (verified: installSkillsToAgent in bot.ts)"
