from django.db import models, transaction
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from util.models.base_models import UUIDPrimaryFieldModel, TimeMonitorModel
from util.mail import mail
import logging

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):

    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        if name := extra_fields.get('name'):
            extra_fields['name'] = self.model.normalize_username(name)
        else:
            extra_fields['name'] = self.model.normalize_username(email.split('@')[0])

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        return user
        
    def _create_user(self, email, password, **extra_fields):
        logger.info(f"Request for new user registeration: {email}")
        send_mail = extra_fields.pop('send_mail', False)

        with transaction.atomic():
            user = self._create_user_object(email, password, **extra_fields)
            user.save()
            EmailVerification = apps.get_model('account.EmailVerification')
            emailverification = EmailVerification.objects.create_emailverification(
                user=user,
                send_mail=send_mail
            )
            emailverification.save()

        logger.info(f"User created: {email}")
        return user
    
    def create_user(self, email, password,  **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('send_mail', True)

        # import ipdb;ipdb.set_trace()
        with transaction.atomic():
            wallet_data = extra_fields.pop("wallet", {})

            user = self._create_user(email, password, **extra_fields)

            # Create wallet
            Wallet = apps.get_model('wallet.Wallet')
            wallet = Wallet.objects.create_wallet(user, **wallet_data)


        return user 
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('send_mail',  False)

        with transaction.atomic():
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

    online_channel = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_online(self):
        return bool(self.online_channel)

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
