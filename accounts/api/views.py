from django.contrib.auth.models import  User
from rest_framework import viewsets
from rest_framework import permissions
from accounts.api.serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
