
from django.contrib.auth.backends import ModelBackend

from .models import Member

class MemberBackend(ModelBackend):
    """Classe MemberBackend pour l'authentification des membres
    """

    def authenticate(self, request, **kwargs):
        """Fonction pour l'authentification d'un membre
            * Vérifie que l'utilisateur existe et que le mot de passe donné est correct

        :parameter request: 
        :parameter kwargs: recupérer les informations de connexion (email et mot de passe)

        :return member: si il existe       
        """

        email = kwargs['email']
        password = kwargs['password']

        try:
            member = Member.objects.get(email=email)
            if password == member.password:
                return member
        except Member.DoesNotExist:
            pass
