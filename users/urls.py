from django.urls import path
from users.views import AdminLoginView, AuthenticatedUserData, ClientLoginView, ClientRegisterView

app_name = "users"

urlpatterns = [
    path("register/",ClientRegisterView.as_view(),name = "register"),   
    path('login/', ClientLoginView.as_view(), name='login-client'),
    path('loginAdmin/', AdminLoginView.as_view(), name='login-admin'),
    path('getuser/<int:id>/', AuthenticatedUserData.as_view(), name='user-data'),
]
