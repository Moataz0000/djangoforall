from django.contrib import admin
from .models import Account, Profile
from django.contrib.auth.admin import UserAdmin




@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username','last_login', 'date_joined', 'is_active']
    list_display_links = ('email', 'first_name','last_name', 'username')
    readonly_fields = ('date_joined', 'last_login')  
    ordering = ['-date_joined']


    filter_horizontal = ()  
    list_filter = ()
    fieldsets = ()
   
   



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
   