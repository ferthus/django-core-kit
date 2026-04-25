from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView


class TokenObtainPairCookieView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                httponly=True,
                secure=True,
                samesite="Lax",
                # domain=".tudominio.com",
            )
            del response.data["refresh"]  # no exponerlo en body

        return response


class TokenRefreshCookieView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            request.data["refresh"] = refresh_token

        return super().post(request, *args, **kwargs)


class LogoutCookieView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.delete_cookie("refresh_token")#, domain=".tudominio.com")

        return response
