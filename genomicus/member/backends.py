
from django.contrib.auth.backends import ModelBackend

from .models import Member

class MemberBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['email']
        password = kwargs['password']

        try:
            member = Member.objects.get(email=email)
            if password == member.password:
                return member
        except Member.DoesNotExist:
            pass