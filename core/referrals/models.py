from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class RefCodes(models.Model):
    code = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Дата публикации")
    expiration = models.DateField(verbose_name='Дата истечения')
    user = models.OneToOneField(User,
                                verbose_name='Создатель',
                                related_name='code')
    

class Invited(models.Model):
    referrer = models.OneToOneField(User,
                                   verbose_name='Пригласивший',
                                   related_name='referrer')
    invitee = models.ForeignKey(User,
                                verbose_name='Приглашенный',
                                related_name='invitee')