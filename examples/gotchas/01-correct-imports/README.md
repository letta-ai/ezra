# Correct Imports

## The Error

```
ModuleNotFoundError: No module named 'letta'
```

## Why It Happens

The Letta SDK package is called `letta-client`, not `letta`. The `letta` package
is the server, not the client SDK.

## Fix

```bash
pip install letta-client
```

```python
# WRONG
from letta import Letta

# RIGHT
from letta_client import Letta
```

## TypeScript

```bash
npm install @letta-ai/letta-client
```

```typescript
import Letta from "@letta-ai/letta-client";
```

## Also Note

- SDK 1.0 uses `api_key`, not `token` (pre-1.0 used `token`)
- No `project_id` needed for Cloud (Jan 2026+)
