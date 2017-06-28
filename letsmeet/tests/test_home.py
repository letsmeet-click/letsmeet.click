import pytest


@pytest.fixture
def generic_menu_items():
    return ['Home', 'All Communities', 'Contact']


def test_home(client, generic_menu_items):
    resp = client.get('/')
    assert resp.status_code == 200

    for menu_item in generic_menu_items + ['Login']:
        assert menu_item.encode() in resp.content


def test_home_logged_in(logged_in_client, generic_menu_items):
    resp = logged_in_client.get('/')
    assert resp.status_code == 200

    for menu_item in generic_menu_items + ['Logout']:
        assert menu_item.encode() in resp.content
