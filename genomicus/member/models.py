from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator


# Create your models here.

#verifiy the form of the phone number
regexNumberTel = RegexValidator(regex = r"0\d (\d{2} ){3}\d{2}")


class MemberManager(models.Manager):
    """Classe MemberManager pour la création d'un nouveau membre
    """

    def create_member(self, email, password, firstName, lastName, phone=''):
        """Fonction create_member
        
        :parameter email: email du nouvel utilisateur
        :parameter password: mot de passe du nouvel utilisateur
        :parameter firstName: prénom du nouvel utilisateur
        :parameter lastName: nom du nouvel utilisateur
        :parameter phone: numéro de téléphone du nouvel utilisateur, de base phone='' si non renseigné
        """
        m = self.create(email=email, password=password, firstName= firstName, lastName=lastName, phone=phone, connecte=False)
        return m

class Member(AbstractBaseUser): 
    """
    Class Member avec toutes les informations sur les membres de l'application

    :parameter email: emailField avec comme pour taille maximal 255, required
    :parameter user_type: un entier {1,2,3,4} correspond à un niveau d'utilisateur {lecteur, annotateur, validateur, admin}
    :parameter firstName: string correspond au prénom de taille maximal 100, required
    :parameter lastName: string correspond au nom de taille maximal 100, required
    :parameter phone: suite de nombres formant un numéro de téléphone devant suivre le format : XX XX XX XX XX, optionnel
    :parameter connecte: boolean : True - connecté sur l'application et False - l'inverse
    :parameter object: MemberManager, crée un nouveau membre
    """
    
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

    connecte = models.BooleanField(editable=False)

    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = MemberManager()