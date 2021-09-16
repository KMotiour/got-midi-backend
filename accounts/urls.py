
from django.urls import path
from .views import UserRUDView, UserInfo

urlpatterns = [

    path('<int:pk>/', UserRUDView.as_view(), name="UpdateUserInfo"),
    path('useinfo/', UserInfo.as_view(), name="UpdateUserInfo")

]
