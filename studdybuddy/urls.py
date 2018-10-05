# users/urls.py
from django.urls import path
from studdybuddy import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.edit, name='edit'),
    path('edit2/', views.edit2, name='edit2'),
    path('profile/', views.profile, name='profile'),
    path('step-1/', views.step1, name='step1'),
    path('step-2/', views.step2, name='step2'),
    path('step-3/', views.step3, name='step3'),
    path('step-4/', views.step4, name='step4'),
    path('step-5/', views.step5, name='step5'),
]
