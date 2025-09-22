from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwner


class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]

    def get(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error":"product not found"},status=404)
        
        self.check_object_permissions(request, products[0])
        serializer = self.serializer_class(products[0])

        return Response(serializer.data,status=200)
    
    def put(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error":"products not found"},status=404)
        
        product = products[0]
        self.check_object_permissions(request, product)

        serializer = self.serializer_class(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        serializer.save()

        return Response(serializer.data,status=200)
    
    def delete(self, request, pk, *args, **kwargs):
        products = Product.objects.filter(id=pk)
        if not products.exists():
            return Response({"error":"product not found"},status=404)
        
        product = products[0]
        self.check_object_permissions(request, product)
        product.delete()

        return Response(status=204)
    
    
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
