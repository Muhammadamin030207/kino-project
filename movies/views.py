from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import CustomUser, Director, Genre, Movie
from .forms import CustomUserCreationForm, LoginForm, DirectorForm, GenreForm, MovieForm


def home_view(request):
    movies = Movie.objects.select_related('director__user').prefetch_related('genres').all()
    return render(request, 'home.html', {'movies': movies})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')


@login_required
def director_profile(request):
    if not hasattr(request.user, 'director_profile'):
        return redirect('director_create')
    director = request.user.director_profile
    movies = director.movies.select_related('director__user').prefetch_related('genres').all()
    return render(request, 'director/profile.html', {'director': director, 'movies': movies})


@login_required
def director_create(request):
    if hasattr(request.user, 'director_profile'):
        return redirect('director_profile')
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            director = form.save(commit=False)
            director.user = request.user
            director.save()
            return redirect('director_profile')
    else:
        form = DirectorForm()
    return render(request, 'director/create.html', {'form': form})


@login_required
def director_edit(request):
    if not hasattr(request.user, 'director_profile'):
        return redirect('director_create')
    director = request.user.director_profile
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            return redirect('director_profile')
    else:
        form = DirectorForm(instance=director)
    return render(request, 'director/edit.html', {'form': form, 'director': director})


@login_required
def director_delete(request):
    if not hasattr(request.user, 'director_profile'):
        return redirect('home')
    director = request.user.director_profile
    if request.method == 'POST':
        director.delete()
        return redirect('home')
    return render(request, 'director/delete.html', {'director': director})


@login_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre/list.html', {'genres': genres})


@login_required
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
    return render(request, 'genre/create.html', {'form': form})


@login_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm(instance=genre)
    return render(request, 'genre/edit.html', {'form': form, 'genre': genre})


@login_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        genre.delete()
        return redirect('genre_list')
    return render(request, 'genre/delete.html', {'genre': genre})


def movie_list(request):
    movies_list = Movie.objects.select_related('director__user').prefetch_related('genres').all().order_by('-created_at')
    paginator = Paginator(movies_list, 6)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movie/list.html', {'movies': movies})


def movie_detail(request, slug):
    movie = get_object_or_404(
        Movie.objects.select_related('director__user').prefetch_related('genres'),
        slug=slug
    )
    return render(request, 'movie/detail.html', {'movie': movie})


@login_required
def movie_create(request):
    if not hasattr(request.user, 'director_profile'):
        messages.warning(request, 'You need a Director profile to create movies.')
        return redirect('director_create')
    director = request.user.director_profile
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.director = director
            if not movie.slug:
                base = slugify(movie.title) or 'movie'
                movie.slug = base
            movie.save()
            form.save_m2m()
            return redirect('movie_detail', slug=movie.slug)
    else:
        form = MovieForm()
    return render(request, 'movie/create.html', {'form': form})


@login_required
def movie_edit(request, slug):
    movie = get_object_or_404(Movie.objects.select_related('director__user'), slug=slug)
    if movie.director.user != request.user:
        return redirect('movie_detail', slug=movie.slug)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', slug=movie.slug)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie/edit.html', {'form': form, 'movie': movie})


@login_required
def movie_delete(request, slug):
    movie = get_object_or_404(Movie.objects.select_related('director__user'), slug=slug)
    if movie.director.user != request.user:
        return redirect('movie_detail', slug=movie.slug)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'movie/delete.html', {'movie': movie})
