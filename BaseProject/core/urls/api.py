from django.urls import path, include

from BaseProject.core.api.views import TokenObtainPairCookieView, TokenRefreshCookieView


urlpatterns = [
    path("token/", TokenObtainPairCookieView.as_view()),
    path("token/refresh/", TokenRefreshCookieView.as_view()),
]
