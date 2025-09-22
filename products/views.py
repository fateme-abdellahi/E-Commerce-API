from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
    