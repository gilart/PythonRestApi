from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .singleton import MetaDataSingleton

class UserDetailView(APIView):
    """
    Endpoint zwracający dane zalogowanego użytkownika.
    Wymaga:
    Authorization: Bearer <access_token>
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        metadata = MetaDataSingleton().get_metadata()
        return Response({"user": serializer.data, "metadata": metadata})

class LogoutView(APIView):
    """
    Endpoint do wylogowania użytkownika - unieważnia refresh token.
    W body requestu należy podać:
    {
       "refresh": "<refresh_token>"
    }
    Wymaga: Authorization: Bearer <access_token>
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Brak refresh tokenu."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            # Blacklist token (unieważnienie)
            token.blacklist()
            return Response({"detail": "Wylogowano pomyślnie."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Nieprawidłowy lub już unieważniony refresh token."}, status=status.HTTP_400_BAD_REQUEST)
