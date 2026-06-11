from django.contrib import admin
from .models import CustomUser, Director, Genre, Movie


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'slug', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'full_name']
    ordering = ['-created_at']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'birth_year']
    search_fields = ['user__full_name', 'country']
    list_filter = ['country']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'release_year', 'rating', 'created_at']
    list_filter = ['genres', 'release_year']
    search_fields = ['title', 'director__user__full_name']
    filter_horizontal = ['genres']
    date_hierarchy = 'created_at'
