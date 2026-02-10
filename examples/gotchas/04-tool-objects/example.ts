/**
 * Correct way to access tool object properties (TypeScript).
 *
 * Tool objects use property access, not bracket notation with strings.
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

const tools = await client.tools.list();

for (const tool of tools.items) {
  // TypeScript naturally uses property access
  console.log(`Tool: ${tool.name}`);
  console.log(`  ID: ${tool.id}`);
}
