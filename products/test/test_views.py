import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_data",
    [
        # correct data
        (
            {
                "name": "Sample Product",
                "description": "This is a sample product",
                "price": 19.99,
                "stock": 50,
                "create_status": 201,
                "update_status": 204,
            }
        ),
        # wrong stock type
        (
            {
                "name": "Sample Product",
                "description": "This is a sample product",
                "price": 19.99,
                "stock": "an string",
                "create_status": 400,
                "update_status": 400,
            }
        ),
        # wrong price type
        (
            {
                "name": "Sample Product",
                "description": "This is a sample product",
                "price": "an string",
                "stock": 50,
                "create_status": 400,
                "update_status": 400,
            }
        ),
        # missing fields
        (
            {
                "description": "This is a sample product",
                "price": 19.99,
                "stock": 50,
                "create_status": 400,
            }
        ),
        # negative price
        (
            {
                "description": "This is a sample product",
                "price": -19.99,
                "stock": 50,
                "create_status": 400,
                "update_status": 400,
            }
        ),
        # negative stock
        (
            {
                "description": "This is a sample product",
                "price": 19.99,
                "stock": -50,
                "create_status": 400,
                "update_status": 400,
            }
        ),
        # missing name
        (
            {
                "description": "This is a sample product",
                "price": 19.99,
                "stock": 0,
                "create_status": 400,
            }
        ),
        # empty name
        (
            {
                "name": "",
                "description": "This is a sample product",
                "price": 19.99,
                "stock": 0,
                "create_status": 400,
            }
        ),
        # no data
        ({"create_status": 400, "update_status": 400}),
        # only update
        ## duplicated name for the same id
        ({"name": "test product", "update_status": 204}),
        ## duplicated name with a different id
        ({"name": "different duplicated name", "update_status": 400}),
    ],
)
class TestProductViews:

    @pytest.mark.create_product
    def test_product_creation(
        self,
        authenticated_admin_client,
        product_create_url,
        product_data,
        get_product_data_by_name,
        create_product,
    ):

        if product_data.get("create_status", None):

            if product_data.get("name") == "duplicated":
                create_product(name="duplicated")
            response = authenticated_admin_client.post(
                product_create_url, product_data, format="json"
            )
            assert response.status_code == product_data["create_status"]

            if response.status_code == 201:

                product = get_product_data_by_name(product_data["name"])

                assert product.name == product_data.get("name")
                assert product.description == product_data.get("description")
                assert float(product.price) == product_data.get("price")
                assert product.stock == product_data.get("stock")

    @pytest.mark.update_product
    def test_product_edit(
        self,
        authenticated_admin_client,
        product_url,
        product_data,
        get_product_data_by_name,
        create_product,
    ):

        if product_data.get("update_status", None):
            old_product_model = create_product(name="test product")

            if product_data.get("name") == "different duplicated name":
                create_product(name="different duplicated name")

            response = authenticated_admin_client.put(
                product_url(old_product_model.id), product_data, format="json"
            )

            assert response.status_code == product_data["update_status"]

            if response.status_code == 204:

                product = get_product_data_by_name(product_data.get("name"))
                assert product.name == product_data.get("name", old_product_model.name)
                assert product.description == product_data.get(
                    "description", old_product_model.description
                )
                assert float(product.price) == product_data.get(
                    "price", old_product_model.price
                )
                assert product.stock == product_data.get(
                    "stock", old_product_model.stock
                )


@pytest.mark.read_product
@pytest.mark.django_db
def test_read_product(authenticated_admin_client, product_url, create_product):
    product = create_product()
    response = authenticated_admin_client.get(product_url(product.id))
    assert response.status_code == 200
    response = authenticated_admin_client.get(product_url(1000))
    assert response.status_code == 404


@pytest.mark.delete_product
@pytest.mark.django_db
def test_delete_product(authenticated_admin_client, product_url, create_product):
    product = create_product()
    response = authenticated_admin_client.delete(product_url(product.id))
    assert response.status_code == 204
    response = authenticated_admin_client.delete(product_url(1000))
    assert response.status_code == 404
