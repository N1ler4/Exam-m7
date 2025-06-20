from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'organization', 'scentific_degree')
    search_fields = ('username', 'email')