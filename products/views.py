from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadonly, IsAdminUser
from .filters import ProductFilter


class ProductAPIView(APIView):
    """
    This view is used to view, update, and delete a product using the product id.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadonly]

    # View a product using it's id
    def get(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            response_data = {
                "result": False,
                "message": "product not found",
            }
            return Response(data=response_data, status=404)
        serializer = self.serializer_class(products[0])

        response_data = {"result": True, "data": serializer.data}

        return Response(data=response_data, status=200)

    # Update a product using it's id
    def put(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            response_data = {
                "result": False,
                "message": "product not found",
            }
            return Response(data=response_data, status=404)

        product = products[0]
        self.check_object_permissions(request, product)

        serializer = self.serializer_class(product, data=request.data, partial=True)
        if not serializer.is_valid():
            response_data = {
                "result": False,
                "message": serializer.errors,
            }
            return Response(data=response_data, status=400)
        serializer.save()

        response_data = {"result": True, "message": "product updated successfully"}
        return Response(data=response_data, status=204)

    # Delete a product using it's id
    def delete(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            response_data = {
                "result": False,
                "message": "product not found",
            }
            return Response(data=response_data, status=404)

        product = products[0]
        self.check_object_permissions(request, product)
        product.delete()

        response_data = {
            "result": True,
            "message": "product deleted successfully",
        }

        return Response(data=response_data, status=204)


class ProductCreateAPIView(APIView):
    """
    This view is used to create a new product for an authenticated user
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serilializer = self.serializer_class(data=request.data)
        if serilializer.is_valid():
            serilializer.save()
            response_data = {
                "result": True,
                "message": "product created successfully",
                "data": serilializer.data,
            }
            return Response(data=response_data, status=201)

        response_data = {
            "result": False,
            "message": serilializer.errors,
        }
        return Response(data=response_data, status=400)


class SearchProductAPIView(APIView):
    """
    This view is used to search for products using query parameters
    such as name, description, price, and the username of the user who created the product
    """

    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()

        product_filter = ProductFilter(request.GET, queryset=queryset)
        if not product_filter.is_valid():
            response_data = {
                "result": False,
                "message": product_filter.errors,
            }
            return Response(data=response_data, status=400)

        serializer = ProductSerializer(product_filter.qs, many=True)

        if serializer.data == []:
            response_data = {
                "result": False,
                "message": "no products found with the given query",
            }
            return Response(data=response_data, status=404)

        response_data = {
            "result": True,
            "message": "products retrieved successfully",
            "data": serializer.data,
        }
        return Response(data=response_data, status=200)
