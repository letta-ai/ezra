/**
 * Correct way to import and initialize the Letta client (TypeScript).
 *
 * Common mistake: importing from wrong package.
 * The SDK package is @letta-ai/letta-client.
 */

// CORRECT - SDK 1.0+
import Letta from "@letta-ai/letta-client";

// Initialize with API key (Letta Cloud)
const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

// For self-hosted servers:
// const client = new Letta({ baseURL: "http://localhost:8283" });

// Verify connection
const agents = await client.agents.list({ limit: 1 });
console.log(`Connected! Found ${agents.items.length} agent(s)`);
