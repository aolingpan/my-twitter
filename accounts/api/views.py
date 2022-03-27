from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer, LoginSerializer, SignUpSerializer
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignUpSerializer

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_login_in': request.user.is_authenticated}
        print(data)
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
            print(data['user'])
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'success': True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    "message": "Please check input",
                    "errors": serializer.errors,
                }, status=400
            )
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # queryset = User.objects.filter(username=username)
        # print(queryset.query)
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                'success': False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(user).data,
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        seriailzer = SignUpSerializer(data=request.data)
        if not seriailzer.is_valid():
            return Response({
                "sucess": False,
                "message": "please check input",
                "errors": seriailzer.errors,
            }, status=400)
        user = seriailzer.save()
        print(user)
        django_login(request, user)
        print(request.data)
        return Response({
            "sucess": True,
            "user": UserSerializer(user).data,
        }, status=201)

