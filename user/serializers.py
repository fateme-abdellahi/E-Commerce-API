from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from user.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        new_user = User.objects.create_user(**validated_data)
        return new_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
