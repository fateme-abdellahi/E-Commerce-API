from django.shortcuts import get_object_or_404
from user.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.permissions import IsAdminUserOrSelf
from utils.utils import get_token


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()

            # login after register
            user = register_serializer.instance
            token = get_token(user)

            return Response({
                'result': True,
                'message':'new user created!',
                'data': {
                    'username': user.username,
                    **token,
                },
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'result': False,
                'message': 'user not created!',
                'data': register_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():

            # login
            user = login_serializer.validated_data['user']
            token = get_token(user)

            return Response({
                'result': True,
                'message': 'login successful!',
                'data': {
                    'username': user.username,
                    **token,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'result': False,
                'message': 'Invalid username or password!',
                'data': login_serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrSelf]

    def get(self, request: Request, user_id):
        user = get_object_or_404(User, id=user_id)

        # check object permission (error 403)
        self.check_object_permissions(request, user)

        profile_serializer = ProfileSerializer(user, context={'request': request}).data
        return Response({
            'result': True,
            'message': 'User profile found!',
            'data': profile_serializer
        }, status=status.HTTP_200_OK)


# logout view