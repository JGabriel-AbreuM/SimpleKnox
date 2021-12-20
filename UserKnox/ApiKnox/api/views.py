from django import http
from django.contrib.auth.models import User
from django.db.models import query
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )

class UserAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "head"]
    permissions_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=self.request.user.id)
            return Response({
                'id': user.id,
                'username': user.username
            })
        except Exception as e:
            return Response({"erro": e})

class LoginAPI(KnoxLoginView):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)