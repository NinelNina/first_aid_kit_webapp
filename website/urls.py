from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('medicine/<int:pk>', views.medicine_description, name='medicine'),
    path('firstaidkit_record/<int:pk>', views.firstaidkit_record, name='firstaidkit_record'),
    path('delete_firstaidkit_record/<int:pk>', views.delete_firstaidkit_record, name='delete_firstaidkit_record'),
    path('add_firstaidkit_record/', views.add_firstaidkit_record, name='add_firstaidkit_record'),
]
