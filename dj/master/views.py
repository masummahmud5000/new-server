from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers  import RegisterSerializer, LoginSerializer, AddMoney
# Create your views here.
# Register ///////////////////////////////////
class register(APIView):
    
    def post(self, request):
        serial = RegisterSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'success': True},status=status.HTTP_200_OK)
        else:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
# Login ///////////////////////////////////
from rest_framework_simplejwt.tokens import RefreshToken

class login(APIView):
    def post(self, request):
        try:
            serial = LoginSerializer(data=request.data)
            if serial.is_valid():

                refresh_token = serial.validated_data['refresh_token']
                access_token = serial.validated_data['access_token']

                response = Response({'success': True}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                )

                return response
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Profile ///////////////////////////////////

class profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # print(user)
            return Response({'username': user.username, 'balance': user.balance, 'userStatus': user.is_staff})
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Add Money ///////////////////////////////////
class addMoney(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:        
            serial = AddMoney(instance=request.user, data=request.data, context={'request': request})

            if serial.is_valid():    
                serial.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
