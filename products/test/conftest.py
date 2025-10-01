import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture(scope="module")
def client():
    return APIClient()


@pytest.fixture
def authenticated_client_factory():
    def _create_authenticated_client(client, is_staff=False):
        user = User.objects.create_user(username="testuser", is_staff=is_staff)
        user.set_password("password")
        user.save()
        client.force_authenticate(user=user)
        return client

    return _create_authenticated_client


@pytest.fixture
def authenticated_admin_client(client, authenticated_client_factory):
    client = authenticated_client_factory(client, is_staff=True)
    return client


@pytest.fixture
def product_data():
    return {
        "name": "Sample Product",
        "description": "This is a sample product",
        "price": 19.99,
        "stock": 50,
    }


@pytest.fixture
def product_create_url():
    return reverse("product-create")
