from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]

    def validate_name(self, value):
        if not self.instance:
            if Product.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    detail="product with this name already exists"
                )
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
