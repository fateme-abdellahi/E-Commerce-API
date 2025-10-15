from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]

    def validate_name(self, value):
        value = value.strip()
        if self.instance is None:
            if Product.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    detail="product with this name already exists"
                )
        else:
            if (
                value != self.instance.name
                and Product.objects.filter(name=value).exists()
            ):
                raise serializers.ValidationError(
                    detail="product with this name already exists"
                )

        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(detail="price can not be negative")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(detail="stock can not be negative")
        return value

    def validate(self, attrs):
        if (
            not attrs.get("name")
            and not attrs.get("description")
            and not attrs.get("price")
            and not attrs.get("stock")
        ):
            raise serializers.ValidationError(detail="inout data can not be empty")
        return attrs

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
