# ==============================================
# api/views.py — Updated with Notifications
# ==============================================
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Room, Reservation, Notification
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer, NotificationSerializer


# ✅ Admin Permission
class IsAdminUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# ✅ Room Management
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUserOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]


# ✅ Reservation Management (auto notifications)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        reservation = serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"✅ Reservation for '{reservation.room.name}' on {reservation.date} confirmed."
        )

    def perform_update(self, serializer):
        reservation = serializer.save()
        Notification.objects.create(
            user=self.request.user,
            message=f"✏️ Reservation for '{reservation.room.name}' on {reservation.date} updated."
        )

    def perform_destroy(self, instance):
        Notification.objects.create(
            user=self.request.user,
            message=f"❌ Reservation for '{instance.room.name}' on {instance.date} cancelled."
        )
        instance.delete()


# ✅ Manage User Accounts
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOnly]


# ✅ Notifications ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


# ✅ Current User Endpoint
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff
    })


# ✅ Register Endpoint
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"error": "Database integrity error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print("❌ Registration error:", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
