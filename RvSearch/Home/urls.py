from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('search/', views.search, name='search'),
    path('search-alternative/', views.search_alternative, name='search-alternative'),
    path('join-as-partner/', views.sitter_registration, name='sitter-registration'),
    path('member/<int:pk>', views.ProfileDetail.as_view(), name='profile-detail'),
]
