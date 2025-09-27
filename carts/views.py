from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CartApiView(APIView):
    def get(self, request):
        # 1. Validate User Token

        # 2. Get User Cart Info

        return Response(
            {
                'result': True,
                'message': 'success',
                'data': []
            }, status=status.HTTP_200_OK
        )
