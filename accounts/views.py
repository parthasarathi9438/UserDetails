from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from knox.models import AuthToken
from accounts.models import Account
from accounts.serializers import RegisterSerializer, UserSerializer, AccountSerializer, ChangePasswordSerializer
from knox.views import LoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import status




class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                         "user": UserSerializer(user).data,
                        "token": AuthToken.objects.create(user)[1]
                        })
        else:
            message = {"error":"Invaid"}
            return Response(message)

class Login(LoginView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            return super(Login, self).post(request, format=None)
        else:
            message = {"error": "try again"}
            return Response(message)


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserCreate(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class ChangePassword(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)