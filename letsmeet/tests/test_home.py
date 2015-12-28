
def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Login" in resp.content
    assert b"Home" in resp.content
    assert b"Communities" in resp.content
    assert b"Contact" in resp.content
