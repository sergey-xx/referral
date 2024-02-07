import requests
from requests.models import PreparedRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from celery import shared_task

from users.models import MailChek


User = get_user_model()


VERIFICATION_URL = 'https://api.hunter.io/v2/email-verifier'
email = 'mcpali4@mail.ru'
params = {'email': email,
          'api_key': settings.API_TOKEN}


@shared_task()
def check_email(email):
    params = {'email': email,
              'api_key': settings.API_TOKEN}
    req = PreparedRequest()
    req.prepare_url(settings.VERIFICATION_URL, params)
    response = requests.get(req.url)
    print(response.text)
    data = response.json().get('data')
    user = get_object_or_404(User, email=email)
    MailChek.objects.get_or_create(
        status=data.get('status'),
        result=data.get('result'),
        score=int(data.get('score')),
        regexp=(data.get('regexp') == 'true'),
        gibberish=(data.get('gibberish') == 'true'),
        disposable=(data.get('disposable') == 'true'),
        webmail=(data.get('webmail') == 'true'),
        mx_records=(data.get('mx_records') == 'true'),
        smtp_server=(data.get('smtp_server') == 'true'),
        smtp_check=(data.get('smtp_check') == 'true'),
        accept_all=(data.get('accept_all') == 'true'),
        block=(data.get('block') == 'true'),
        user=user
    )
