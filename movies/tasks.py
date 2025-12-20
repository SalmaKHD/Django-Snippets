from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_movie_added_email(movie_title):
    send_mail(
        subject='New Movie Added',
        message=f'A new movie "{movie_title}" was added to the store!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['admin@yourstore.com'],
        fail_silently=False,
    )