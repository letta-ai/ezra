"""Test: Pagination patterns."""


def test_pagination_has_items(client):
    """Verify list endpoints return page objects with .items."""
    page = client.agents.list(limit=1)
    assert hasattr(page, "items"), "Page should have .items"
    assert isinstance(page.items, list), ".items should be a list"


def test_tools_pagination(client):
    """Verify tools list also uses page objects."""
    page = client.tools.list()
    assert hasattr(page, "items"), "Tools page should have .items"
