from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator


# Create your models here.

#verifiy the form of the phone number
regexNumberTel = RegexValidator(regex = r"0\d (\d{2} ){3}\d{2}")


class MemberManager(models.Manager):
    def create_member(self, email, password, firstName, lastName, phone=''):
        m = self.create(email=email, password=password, firstName= firstName, lastName=lastName, phone=phone, connecte=False)
        return m

class Member(AbstractBaseUser): 
    #email - primary key
    #email = models.EmailField(max_length=255, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)

    #user type
    USER_TYPE_CHOICES = (
        (1, 'lecteur'),
        (2, 'annotateur'),
        (3, 'validateur'),
        (4, 'admin')
    ) 
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    #First + Last Name
    firstName  = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)


    #telephone number
    phone = models.CharField(validators=[regexNumberTel], max_length=14,blank=True) 

    #specify the connexion field
    USERNAME_FIELD = 'email'

    connecte = models.BooleanField()

    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = MemberManager()