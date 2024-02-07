from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        print('тестовая команда выполнена!')
