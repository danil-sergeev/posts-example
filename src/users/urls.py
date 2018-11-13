from django.urls import path

from users import views


app_name = 'users'
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('retrieve-user/<int:pk>', views.RetrieveUserAPIView.as_view(), name='retrieve-user'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout')
]
