from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("token",TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/",TokenRefreshView.as_view(), name="token_refresh"),
    path('transaction/',include('transactions.urls', namespace="transactions")),
    path('users/',include('users.urls', namespace="users")), 
]

# urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()