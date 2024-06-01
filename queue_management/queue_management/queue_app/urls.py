from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile
urlpatterns = [
    path('', views.home, name='home'),
    path('queue_status/', views.queue_status, name='queue_status'),
    path('invite_next/', views.invite_next, name='invite_next'),
    path('direct_to_desk/<int:desk>/', views.direct_to_desk, name='direct_to_desk'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/home.html', views.home, name='profile_home'),
   path('allocate_next_user/', views.allocate_next_user, name='allocate_next_user'),
]
