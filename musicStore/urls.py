"""musicStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import terminal_size
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import MyTokenObtainPairView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')),
    path('user/', include('accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', MyTokenObtainPairView.as_view(), name="apiToken" ),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('/api/password_reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]