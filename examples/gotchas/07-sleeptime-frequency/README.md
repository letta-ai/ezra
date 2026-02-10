# Sleeptime Frequency

## The Error

No error - the change is **silently ignored**.

## Why It Happens

The `sleeptime_agent_frequency` must be nested inside `manager_config`.
Passing it as a top-level parameter to `groups.update()` does nothing.

## Fix

```python
# WRONG - silently ignored
client.groups.update(group_id, sleeptime_agent_frequency=25)

# RIGHT - nested in manager_config
client.groups.update(
    group_id,
    manager_config={
        "manager_type": "sleeptime",
        "sleeptime_agent_frequency": 25,
    },
)
```

## Getting the Group ID

```python
agent = client.agents.retrieve(agent_id)
group_id = agent.multi_agent_group.id
```

## What is sleeptime_agent_frequency?

Controls how many messages trigger the sleeptime agent to run.
Default is typically 10. Set to 25 for less frequent background processing.

Both `interval_seconds` and `min_messages` must be met for sleeptime to trigger.
