# ======================================
# backend/urls.py — Main Project URLs
# ======================================

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ✅ Default Django admin panel
    path('admin/', admin.site.urls),

    # ✅ API routes (your custom app endpoints)
    path('api/', include('api.urls')),

    # ✅ JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
