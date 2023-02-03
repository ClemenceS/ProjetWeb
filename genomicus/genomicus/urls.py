from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('', include('genomApp.urls')),
    path('',include('member.urls')),

    path('admin/', admin.site.urls),
]
