
def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Login' in resp.content
    assert b'Home' in resp.content
    assert b'Communities' in resp.content
    assert b'Contact' in resp.content


def test_home_logged_in(logged_in_client):
    resp = logged_in_client.get('/')
    assert resp.status_code == 200
    print('DEBUG', vars(resp).keys())
    assert b'Logout' in resp.content
    assert b'Home' in resp.content
    assert b'Communities' in resp.content
    assert b'Contact' in resp.content
