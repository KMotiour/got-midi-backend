from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import NewUsers
from .serializers import UserSerializer
# Create your views here.
class UserRUDView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset=NewUsers.objects.all()


class UserInfo(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    def get_queryset(self):
        user_id = self.request.user.id
        print(user_id)
        queryset=NewUsers.objects.filter(id=user_id)

        return queryset
    



