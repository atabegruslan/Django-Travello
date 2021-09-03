# https://www.youtube.com/watch?v=Wq6JqXqOzCE&list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV&index=9&t=510s
# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/models/

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

# https://www.django-rest-framework.org/api-guide/authentication/#by-using-signals
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# https://stackoverflow.com/questions/22134895/django-logging-to-console/22141937#22141937
import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('User must have an email address')
		if not username:
			raise ValueError('User must have an email username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
		)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)	
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	first_name = models.CharField(verbose_name="first name", max_length=30, blank=True)
	last_name = models.CharField(verbose_name="last name", max_length=30, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta():
		db_table = '"auth_user"'

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

@receiver(post_save, sender=Account) # settings.AUTH_USER_MODEL
def create_auth_token(sender, instance=None, created=False, **kwargs):

	logging.config.dictConfig(LOGGING)
	logging.info('-- Inside create_auth_token --')
	logging.info(instance)

	# if created:
	# 	Token.objects.create(user=instance)

	user = User.objects.get(email=instance)
	Token.objects.create(user=user)
