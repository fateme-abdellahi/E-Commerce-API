import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ..models import Product


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
def get_product_data_by_name():
    def _get_product_data(name):
        return Product.objects.filter(name=name)[0]

    return _get_product_data


@pytest.fixture
def product_create_url():
    return reverse("product-create")


# product url for update read delete
@pytest.fixture
def product_url():
    def _get_id(id):
        return reverse(
            "product",
            args=[
                id,
            ],
        )

    return _get_id


@pytest.fixture
def create_product():
    def _create_product(
        name="product", price=1.00, description="a new product", stock=1
    ):
        return Product.objects.create(
            name=name, price=price, description=description, stock=stock
        )

    return _create_product
