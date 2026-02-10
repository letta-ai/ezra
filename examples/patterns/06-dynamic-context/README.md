# Dynamic Context Loading

## Pattern

Agents that load and unload their own memory blocks at runtime.

## Tool: `note` by Cameron Pfiffer

https://github.com/cpfiffer/note

A custom tool that gives agents a file system for their memory blocks.
Agents store notes, then selectively attach them to context when needed.

## Install

```bash
curl -sSL https://raw.githubusercontent.com/cpfiffer/note/main/install.sh | bash
```

## Key Commands

| Command | Description |
|---------|-------------|
| `note attach /path` | Load note into agent context |
| `note detach /path` | Remove from context (keeps in storage) |
| `note create /path` | Create note without attaching |
| `note list` | List all notes |
| `note search query` | Search notes by content |
| `note attached` | Show currently loaded notes |

## Use Cases

- **Progressive disclosure**: Load detailed docs only when relevant
- **Context optimization**: Keep context lean by detaching unused blocks
- **Agent-managed knowledge**: Agent decides what to load for each task

## Important Notes

- Notes ARE memory blocks (with path-like labels)
- Attach = in context (costs tokens), Detach = stored but not in context
- A `/note_directory` block is auto-maintained showing all notes
- Changes persist across conversations
