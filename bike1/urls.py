from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_reg),
    
    path('login', views.login),

    path('register', views.register_user),

    path('dashboard', views.dashboard),

    path('logout', views.logout),

    path('gallery', views.gallery),

    path('upload_pic', views.upload_pic),
]