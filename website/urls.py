from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('medicine/', views.medicine_list, name='medicine_list'),
    path("medicine/search/", views.search_medicine, name="medicine_search"),
    path('disease/', views.diseases_list, name='diseases_list'),
    path("disease/search/", views.search_disease, name="disease_search"),
    # path('symptom/', views.symptoms_list, name='symptoms_list'),
    path('symptom/', views.search_disease_by_symptom, name='disease_by_symptom_search'),
    path('my_firstaidkit/', views.firstaidkit, name='firstaidkit'),
    path("my_firstaidkit/search/", views.search_firstaidkit, name="firstaidkit_search"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('medicine/<int:pk>', views.medicine_description, name='medicine'),
    path('disease/<str:pk>', views.disease_description, name='disease'),
    path('delete_firstaidkit_record/<int:pk>', views.delete_firstaidkit_record, name='delete_firstaidkit_record'),
    path('update_firstaidkit_record/<int:pk>', views.update_firstaidkit_record, name='update_firstaidkit_record'),
    path('add_firstaidkit_record/', views.add_firstaidkit_record, name='add_firstaidkit_record'),
]
