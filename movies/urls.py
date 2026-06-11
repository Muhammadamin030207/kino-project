from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('director/profile/', views.director_profile, name='director_profile'),
    path('director/create/', views.director_create, name='director_create'),
    path('director/edit/', views.director_edit, name='director_edit'),
    path('director/delete/', views.director_delete, name='director_delete'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/create/', views.genre_create, name='genre_create'),
    path('genres/<int:pk>/edit/', views.genre_edit, name='genre_edit'),
    path('genres/<int:pk>/delete/', views.genre_delete, name='genre_delete'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/create/', views.movie_create, name='movie_create'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('movies/<slug:slug>/edit/', views.movie_edit, name='movie_edit'),
    path('movies/<slug:slug>/delete/', views.movie_delete, name='movie_delete'),
]
