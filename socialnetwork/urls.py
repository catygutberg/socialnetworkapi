from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import PostView, UserNewView, UserInfoView, LikeView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/post/", PostView.as_view()),

    path("api/user/new/", UserNewView.as_view()),
    path("api/user/info/", UserInfoView.as_view()),

    path("api/like/", LikeView.as_view()),

    path('api/session/new/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/session/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
