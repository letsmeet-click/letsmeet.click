import pytest
from django.utils import timezone


@pytest.fixture
def logged_in_user(django_user_model):
    user = django_user_model.objects.create_user(
        username='dummy_user',
        email='dummy@example.org',
        password='dummypass',
        last_login=timezone.now(),
    )
    user.set_password('dummypass')
    user.save()

    yield user

    user.delete()


@pytest.fixture
def logged_in_client(client, logged_in_user):
    client.force_login(
        logged_in_user,
        backend='django.contrib.auth.backends.ModelBackend',
    )
    return client
