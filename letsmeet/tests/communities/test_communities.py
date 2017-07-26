from django.urls import reverse


table_headers = [
    'Community',
    'Your Role',
    'Subscribers',
    'Next event',
]


def test_communities_anonymous(
        client, generic_community, deleted_community, subscribed_community,
):
    resp = client.get('/c/')
    assert resp.status_code == 200

    _check_communites_common(resp.content, [generic_community, subscribed_community])

    assert resp.content.count('<td>Not subscribed</td>'.encode()) == 2
    assert resp.content.count('<td>Subscriber</td>'.encode()) == 0


def test_communities(
        logged_in_client, generic_community, deleted_community,
        subscribed_community,
):
    resp = logged_in_client.get('/c/')
    assert resp.status_code == 200

    _check_communites_common(resp.content, [generic_community, subscribed_community])

    assert resp.content.count('<td>Not subscribed</td>'.encode()) == 1
    assert resp.content.count('<td>Subscriber</td>'.encode()) == 1


def _check_communites_common(content, communities):
    assert f'<noscript>{len(communities)}</noscript> communities'.encode() in content

    for table_header in table_headers:
        assert table_header.encode() in content

    for community in communities:
        assert community.name.encode() in content
        community_link = reverse('community_detail', args=(community.slug, ))
        assert f"location='{community_link}';" in content.decode('utf-8')

    assert content.count('No upcoming event'.encode()) == len(communities)
