from django.contrib import admin
from .models import Product, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
