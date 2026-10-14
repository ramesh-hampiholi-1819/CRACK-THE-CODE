from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('languages/', views.languages, name='languages'),
    path('language/<slug:slug>/', views.language_detail, name='language_detail'),
    path('practice/', views.practice, name='practice'),
    path('execute/', views.execute_code, name='execute_code'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenge/<slug:slug>/', views.challenge_detail, name='challenge_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
]
