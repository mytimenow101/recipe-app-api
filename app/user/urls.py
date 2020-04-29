from django.urls import path
from user import views



app_name = 'user'



urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.MangeUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]