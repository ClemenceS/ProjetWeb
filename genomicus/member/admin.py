from django.contrib import admin

#import the class Member
from .models import Member

# Register your models here.
class MembersAdmin(admin.ModelAdmin):
    readonly_fields = ["connecte"]
    #pass
admin.site.register(Member, MembersAdmin)