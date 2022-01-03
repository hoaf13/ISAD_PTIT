from django.urls import path
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.decorators import login_required
from .views import ValidateUser

urlpatterns = [
    path("validate/", ValidateUser.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login-view'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login-view'), name='logout-view'),
]