import pytest


class TestCreateProductViews:
    # @pytest.mark.parametrize("")

    @pytest.mark.django_db
    def test_product_correct_inputs(
        self, authenticated_admin_client, product_data, product_create_url
    ):
        response = authenticated_admin_client.post(
            product_create_url, product_data, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == product_data["name"]
        assert response.data["description"] == product_data["description"]
        assert float(response.data["price"]) == product_data["price"]
        assert response.data["stock"] == product_data["stock"]

    # @pytest.mark.django_db
    # def test_example(self):
    #     assert True


# from products.views import the_test_one
# from unittest.mock import Mock
# def test_the_real_one():
#     Mock().patch('E-Commerce-API.products.views.mocked', return_value="the mocked value")
#     assert the_test_one() == "the mocked value"
