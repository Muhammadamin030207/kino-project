from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import CustomUser, Genre, Movie


@receiver(pre_save, sender=CustomUser)
def create_user_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.full_name)
        if not base_slug:
            base_slug = slugify(instance.email.split('@')[0])
        instance.slug = base_slug


@receiver(pre_save, sender=Genre)
def create_genre_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Movie)
def create_movie_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        counter = 1
        while Movie.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug
