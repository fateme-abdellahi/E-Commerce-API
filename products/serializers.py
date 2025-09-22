from rest_framework.serializers import ModelSerializer
from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
