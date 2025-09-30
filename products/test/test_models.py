import pytest
from ..models import Product

@pytest.mark.django_db
def test_product_model(product_data):
    product = Product.objects.create(**product_data)
    assert product.name == product_data['name']
    assert product.description == product_data['description']
    assert product.price == product_data['price']
    assert product.stock == product_data['stock']