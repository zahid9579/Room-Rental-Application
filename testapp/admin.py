from django.contrib import admin
from .models import Room, Booking, Review, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model
    # These override the definitions on the base UserAdmin
    list_display = ["email", "name", "tc", "is_admin"]  # Fixed missing comma
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is used for creating a new user
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# Register the custom UserAdmin
admin.site.register(User, UserModelAdmin)
