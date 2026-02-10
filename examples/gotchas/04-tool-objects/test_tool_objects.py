"""Test: Tool object attribute access."""

import pytest


def test_tool_dot_notation(client):
    """Verify tool objects use dot notation."""
    tools = client.tools.list()
    if tools.items:
        tool = tools.items[0]
        # These should work (dot notation)
        assert tool.name is not None
        assert tool.id is not None

        # This should fail (dict notation)
        with pytest.raises(TypeError):
            _ = tool["name"]
