from django.urls import path

from users.views import AdminLoginView, AuthenticatedUserData, AuthenticatedUserDataa, BankClientUpdateView, ClientLoginView, ClientRegisterView, PushNotificationView, change_password

app_name = "users"


urlpatterns = [
    path('push-notification/', PushNotificationView.as_view(), name='push_notification'),
    path("register/",ClientRegisterView.as_view(),name = "register"),   
    path('login/', ClientLoginView.as_view(), name='login-client'),
    path('loginAdmin/', AdminLoginView.as_view(), name='login-admin'),
    path('getuser/<int:id>/', AuthenticatedUserData.as_view(), name='user-data'),
    path('upload/<int:id>/', BankClientUpdateView.as_view(), name='image'),
    path('me/', AuthenticatedUserDataa.as_view(), name='user-data'),
    path('changepassword/', change_password,),




]
