from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search-alternative/', views.search_alternative, name='search-alternative'),
    path('join-as-partner/', views.sitter_registration, name='sitter-registration'),
    path('member/<int:pk>', views.profile_detail, name='profile-detail'),
    path('test/', views.test, name='test'),
]
