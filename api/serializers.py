# ==============================================
# api/serializers.py — Updated with NotificationSerializer
# ==============================================
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Reservation, Notification


# -------------------------------
# USER SERIALIZER
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]


# -------------------------------
# ROOM SERIALIZER
# -------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


# -------------------------------
# RESERVATION SERIALIZER
# -------------------------------
class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source="room",
        write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "room",
            "room_id",
            "date",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]
        read_only_fields = ["user", "status", "created_at"]


# -------------------------------
# NOTIFICATION SERIALIZER
# -------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "created_at", "read"]
