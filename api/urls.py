# ======================================
# api/urls.py — Updated with Notifications
# ======================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RoomViewSet,
    ReservationViewSet,
    UserViewSet,
    NotificationViewSet,
    current_user,
    register_user,
)

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"users", UserViewSet, basename="user")
router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
    path("current_user/", current_user, name="current_user"),
    path("register/", register_user, name="register_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
