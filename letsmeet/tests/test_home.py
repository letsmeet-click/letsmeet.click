generic_menu_items = [
    'Home', 'All Communities', 'Contact', 'About/FAQ', 'Legal/Contact',
]


logged_out_menu_items = ['Login']
logged_in_menu_items = ['Logout']


advertisements = [
    'No registration required',
    'Organize your event attendees',
    'Use your existing communication channels',
    'It\'s free',
    'Kickstart your event',
]


dashboard = [
    'You have no upcoming events.',
    'You currently have no active community subscriptions.',
    '<noscript>0</noscript> Communities',
    '<noscript>0</noscript> upcoming confirmed events',
    'Currently no upcoming events',
]


def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

    for menu_item in generic_menu_items + logged_out_menu_items:
        assert menu_item.encode() in resp.content

    for menu_item in logged_in_menu_items:
        assert menu_item.encode() not in resp.content

    for advertisement in advertisements:
        assert advertisement.encode() in resp.content

    for item in dashboard:
        assert item.encode() not in resp.content


def test_home_logged_in(logged_in_client):
    resp = logged_in_client.get('/')
    assert resp.status_code == 200

    for menu_item in generic_menu_items + logged_in_menu_items:
        assert menu_item.encode() in resp.content

    for menu_item in logged_out_menu_items:
        assert menu_item.encode() not in resp.content

    for advertisement in advertisements:
        assert advertisement.encode() not in resp.content

    for item in dashboard:
        assert item.encode() in resp.content
