from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
	phone = models.CharField(max_length=30, verbose_name='Номер телефона', unique=True)


class UserLoginCode(models.Model):
	user = models.OneToOneField(User, related_name='user_code', on_delete=models.CASCADE, verbose_name=_('User'))
	login_code = models.CharField(max_length=6, verbose_name=_('Code'))

