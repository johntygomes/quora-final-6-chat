from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=40, unique=True, null=False)
    email = models.EmailField(_('email address'), unique=True, null=False)
    auth_type = models.CharField(_('auth_type'), max_length=20, default="email")
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('is_verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None,created=False,**kwargs):
  if created:
    Token.objects.create(user=instance)


class EmailVerificationTokenModel(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
  token = models.UUIDField()
  created_time = models.DateTimeField(_('time_created'), auto_now_add=True)
  created_time_in_seconds = models.IntegerField(_('created_time_in_seconds'))

class GoogleUserPasswordModel(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="googleuser")
  plain_text_password = models.CharField(max_length=255)


