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
            return Response(status=404)
        
        serializer = self.serializer_class(products[0])

        return Response(serializer.data)
    
    
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
