from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель Пользователей."""

    email = models.EmailField('email адрес', blank=False, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)



class MailChek(models.Model):

    status = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    score = models.IntegerField()
    regexp = models.BooleanField()
    gibberish = models.BooleanField()
    disposable = models.BooleanField()
    webmail = models.BooleanField()
    mx_records = models.BooleanField()
    smtp_server = models.BooleanField()
    smtp_check = models.BooleanField()
    accept_all = models.BooleanField()
    block = models.BooleanField()
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                blank=True)
