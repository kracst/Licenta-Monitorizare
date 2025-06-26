from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about/',views.about,name="about"),
    path('create/', ProjectCreateView.as_view(),name="create"),
    path('edit/<int:pk>', ProjectEditView.as_view(),name="edit"),
    path('delete/<int:pk>', ProjectDeleteView.as_view(),name="delete"),
    path('api/receive_data/', receive_data, name='receive_data'),
    path('api/get_sensor_data/', views.get_sensor_data, name='get_sensor_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]
