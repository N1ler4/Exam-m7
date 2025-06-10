from django.urls import path
from .views import ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView , ShowProfileView, UpdateUserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("password-reset/", PasswordResetRequestView.as_view(),
         name="password_reset_request"),
    path("password-reset-confirm/<int:pk>/<str:token>/",
         PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("profile/", ShowProfileView.as_view(), name="show_profile"),
    path("update-profile/", UpdateUserProfileView.as_view(), name="update_profile"),
]
