from django.db import models
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.mail import mail

class UserManager(BaseUserManager):

    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        if name := extra_fields.get('name'):
            extra_fields['name'] = self.model.normalize_username(name)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        return user
        
    def _create_user(self, email, password, **extra_fields):
        send_mail = extra_fields.pop('send_mail', False)

        user = self._create_user_object(email, password, **extra_fields)
        user.save()
        EmailVerification = apps.get_model('account.EmailVerification')
        emailverification = EmailVerification(
            user=user,
        )
        emailverification.save()

        if send_mail:
            user.send_verification_mail()

        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('send_mail', True)

        user = self._create_user(email, password, **extra_fields)
        return user 
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('send_mail',  False)

        user = self.create_user(email, password, **extra_fields)
        user.emailverification.verify(force=True)
        return user

class User(AbstractBaseUser, PermissionsMixin, UUIDPrimaryFieldModel, TimeMonitorModel):

    class Genders(models.TextChoices):
        male = 'Male'
        female = 'Female'
        other = 'Other'

    email = models.EmailField(
        unique=True
    )

    image = models.ImageField(
        upload_to='profile/',
        default='profile/user-image.jpg', 
    )

    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    gender = models.CharField(
        choices=Genders,
        max_length=12,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        db_default=True,
    )

    is_staff = models.BooleanField(
        db_default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def create_email_verification_code(self, force=False):
        from account.models import EmailVerification
        if self.emailverification:
            if force:
                self.emailverification.delete()
            return False

        emailverification = EmailVerification(
            user=self,
        )
        emailverification.save()
        return emailverification.code.hex

    def create_refresh_token(self):
        """After validating properly, it created refresh token
        in db otherwise returns False
        
        """

        from account.models import RefreshToken
        # Check if there are not more than x tokens already
        if self.tokens.count() >= settings.TOKEN_REFRESH_MAX_NUMBER_IN_DB:
            return False

        # Create new token
        token = RefreshToken(
            user=self
        )
        token.save()
        return token
        


            

    def send_verification_mail(self):

        return mail(
            subject='Testing', 
            message='We are testing bro', 
            recipient_list=[self.email],
            html_message='<h1>We are testing bro</h1>',
            fail_silently=True,
        )
