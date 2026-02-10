"""Test: Correct imports and client initialization."""


def test_import_and_connect(client):
    """Verify the client can connect and list agents."""
    agents = client.agents.list(limit=1)
    assert hasattr(agents, "items"), "Response should have .items attribute"
