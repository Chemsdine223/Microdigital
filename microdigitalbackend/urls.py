from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
# from rest_framework_swagger.views import get_swagger_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
schema_view = get_schema_view(
    openapi.Info(
        title="Swagger First Blog ",
        default_version='v1',
        description="Test Swagger First Blog",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@swaggerBlog.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("token",TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/",TokenRefreshView.as_view(), name="token_refresh"),
    path('transaction/',include('transactions.urls', namespace="transactions")),
    path('users/',include('users.urls', namespace="users")), 
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),]

# urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()