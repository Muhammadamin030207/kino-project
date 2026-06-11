from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
from django.urls import reverse


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class Director(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='director_profile')
    country = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='directors/', blank=True, null=True)
    awards = models.TextField(blank=True)

    def __str__(self):
        return self.user.full_name

    def get_absolute_url(self):
        return reverse('director_profile')


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre_list')


class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    release_year = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            if not base:
                base = 'movie'
            self.slug = base
            counter = 1
            while Movie.objects.filter(slug=self.slug).exists():
                self.slug = f'{base}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})
