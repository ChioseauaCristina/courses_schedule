from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('', views.index, name="courses"),
    path('update_course/<str:pk>/', views.update_course, name="update_course"),
    path('delete_course/<str:pk>/', views.delete_course, name="delete_course"),
]
