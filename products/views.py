from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend


class ProductAPIView(APIView):
    """
    This view is used to view, update, and delete a product using the product id.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsOwner]

    # View a product using it's id
    def get(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error": "product not found"}, status=404)
        serializer = self.serializer_class(products[0])

        return Response(serializer.data, status=200)

    # Update a product using it's id
    def put(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error": "products not found"}, status=404)

        product = products[0]
        self.check_object_permissions(request, product)

        serializer = self.serializer_class(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()

        return Response(serializer.data, status=200)

    # Delete a product using it's id
    def delete(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error": "product not found"}, status=404)

        product = products[0]
        self.check_object_permissions(request, product)
        product.delete()

        return Response(status=204)


class ProductCreateAPIView(generics.CreateAPIView):
    """
    This view is used to create a new product for an authenticated user
    """

    serializer_class = ProductSerializer
    permission_classes = [IsOwner]


class SearchProductAPIView(generics.ListAPIView):
    """
    This view is used to search for products using query parameters
    such as name, description, price, and the username of the user who created the product
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "description", "price", "owner__username", "stock"]
