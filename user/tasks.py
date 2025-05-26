from cinemas.celery import app
from django.core.mail import send_mail
from django.conf import settings

@app.task
def send_email(email, code):
    send_mail(
        'Ваш код підтвердження для відновлення паролю',
        f'Ваш код підтвердження: {code}',
        settings.EMAIL_HSOT_USER,
        [email],
        fail_silently=False
    )