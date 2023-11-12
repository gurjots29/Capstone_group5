from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Volunteer, Badge, Skill, Organization, OrganizationMembership


class FollowersInline(admin.TabularInline):
    model = User.following.through
    fk_name = "from_user"
    verbose_name = "I am following some people"
    verbose_name_plural = f"{verbose_name}"


class FollowingInline(admin.TabularInline):
    model = User.following.through
    fk_name = "to_user"
    verbose_name = "Some people are following me"
    verbose_name_plural = f"{verbose_name}"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ("username", "password"),
            },
        ),
        ("Info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Info Addition",
            {
                "fields": ("profile_image", "background_image", "headline"),
            },
        ),
        # (
        #     "Like",
        #     {
        #         "fields": ("like_posts",),
        #     },
        # ),
        (
            "Authority",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Date",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    ]
    inlines = [
        FollowersInline,
        FollowingInline,
    ]


admin.site.register(Volunteer)
admin.site.register(Badge)
admin.site.register(Skill)
admin.site.register(Organization)
admin.site.register(OrganizationMembership)