from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_firstaidkit/', views.firstaidkit, name='firstaidkit'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('medicine/<int:pk>', views.medicine_description, name='medicine'),
    path('delete_firstaidkit_record/<int:pk>', views.delete_firstaidkit_record, name='delete_firstaidkit_record'),
    path('update_firstaidkit_record/<int:pk>', views.update_firstaidkit_record, name='update_firstaidkit_record'),
    path('add_firstaidkit_record/', views.add_firstaidkit_record, name='add_firstaidkit_record'),
]
