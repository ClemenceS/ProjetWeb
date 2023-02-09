from django.contrib import admin

#import the class Member
from .models import Member

# Register your models here.
class MembersAdmin(admin.ModelAdmin):
    """Spécifie que le champ connecte ne peut qu'être vu par l'administrateur, il n'a pas le droit de le modifier
    """

    readonly_fields = ["connecte"]

admin.site.register(Member, MembersAdmin)