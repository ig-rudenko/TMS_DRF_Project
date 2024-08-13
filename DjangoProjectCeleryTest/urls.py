"""
URL configuration for DjangoProjectCeleryTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Определяем список URL-маршрутов
urlpatterns = [
    # Маршрут для панели администратора Django
    path('admin/', admin.site.urls),

    # Включаем URL-маршруты из приложения 'app.api.urls' под префиксом 'api/v1/posts/'
    path("api/v1/posts/", include("app.api.urls")),

    # Маршрут для получения JWT-токена
    path("api/v1/token", TokenObtainPairView.as_view(), name="obtain-token"),
    # Маршрут для обновления JWT-токена
    path("api/v1/token/refresh", TokenRefreshView.as_view(), name="refresh-token"),
    # Маршрут для проверки JWT-токена
    path("api/v1/token/verify", TokenVerifyView.as_view(), name="verify-token"),
]

# Добавляем маршруты для Django Debug Toolbar, если включен режим отладки
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
