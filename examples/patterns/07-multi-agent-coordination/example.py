"""Multi-agent coordination: Client-side orchestration with shared state.

Pattern: Multiple specialized agents coordinated by application code,
sharing state through shared memory blocks. Letta's recommended approach
over server-side agent groups.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Create shared state blocks ---

task_board = client.blocks.create(
    label="task_board",
    value="Tasks:\n- [ ] Research memory patterns\n- [ ] Write example code\n- [ ] Review results",
)

findings = client.blocks.create(
    label="findings",
    value="No findings yet.",
)

print(f"Task board block: {task_board.id}")
print(f"Findings block: {findings.id}")

# --- Create specialized agents ---

researcher = client.agents.create(
    name="researcher_agent",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am a research agent. I analyze topics and record findings in the 'findings' block.",
        },
        {"label": "human", "value": "The orchestrator coordinating my work."},
    ],
)

# Attach shared blocks
client.agents.blocks.attach(task_board.id, agent_id=researcher.id)
client.agents.blocks.attach(findings.id, agent_id=researcher.id)

writer = client.agents.create(
    name="writer_agent",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am a writing agent. I read findings and produce clear documentation.",
        },
        {"label": "human", "value": "The orchestrator coordinating my work."},
    ],
)

# Attach same shared blocks
client.agents.blocks.attach(task_board.id, agent_id=writer.id)
client.agents.blocks.attach(findings.id, agent_id=writer.id)

print(f"Researcher: {researcher.id}")
print(f"Writer: {writer.id}")

# --- Client-side orchestration ---

# Step 1: Researcher analyzes a topic
print("\n=== Step 1: Research ===")
research_response = client.agents.messages.create(
    agent_id=researcher.id,
    messages=[{
        "role": "user",
        "content": "Research how Letta memory blocks work. Write your findings to the 'findings' block.",
    }],
)

for msg in research_response.messages:
    if msg.message_type == "assistant_message":
        print(f"Researcher: {msg.content[:150]}...")

# Step 2: Writer reads findings and produces documentation
print("\n=== Step 2: Writing ===")
writer_response = client.agents.messages.create(
    agent_id=writer.id,
    messages=[{
        "role": "user",
        "content": "Read the 'findings' block and summarize the research into a brief paragraph.",
    }],
)

for msg in writer_response.messages:
    if msg.message_type == "assistant_message":
        print(f"Writer: {msg.content[:150]}...")

# --- Check final state ---

print("\n=== Final Shared State ===")
final_findings = client.blocks.retrieve(findings.id)
print(f"Findings: {final_findings.value[:200]}")

# --- Cleanup ---

client.agents.blocks.detach(task_board.id, agent_id=researcher.id)
client.agents.blocks.detach(findings.id, agent_id=researcher.id)
client.agents.blocks.detach(task_board.id, agent_id=writer.id)
client.agents.blocks.detach(findings.id, agent_id=writer.id)
client.agents.delete(researcher.id)
client.agents.delete(writer.id)
client.blocks.delete(task_board.id)
client.blocks.delete(findings.id)
