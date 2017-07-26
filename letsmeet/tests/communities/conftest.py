import pytest

from communities.models import Community


@pytest.fixture
def generic_community(transactional_db):
    community = Community.objects.create(
        name='Example Community',
    )

    yield community

    community.delete()


@pytest.fixture
def deleted_community(transactional_db):
    community = Community.objects.create(
        name='Deleted Community',
        is_deleted=True,
    )

    yield community

    community.delete()


@pytest.fixture
def subscribed_community(logged_in_user):
    community = Community.objects.create(
        name='Subscribed Community',
    )
    community.subscribe_user(logged_in_user)

    yield community

    community.delete()
