/**
 * Correct way to paginate through Letta API results (TypeScript).
 *
 * SDK 1.0+ uses cursor-based pagination. Results come in a page object
 * with an .items property.
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

// Results come in a page object with .items
const page = await client.agents.list({ limit: 5 });
console.log(`Got ${page.items.length} agents`);

for (const agent of page.items) {
  console.log(`  ${agent.name} (${agent.id})`);
}

// Cursor-based pagination
const firstPage = await client.agents.list({ limit: 3 });
console.log(`\nFirst page: ${firstPage.items.length} agents`);

if (firstPage.items.length > 0) {
  const lastId = firstPage.items[firstPage.items.length - 1].id;
  const secondPage = await client.agents.list({ limit: 3, after: lastId });
  console.log(`Second page: ${secondPage.items.length} agents`);
}
