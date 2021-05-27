from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter
from django.utils.html import format_html

from .models import User, CustomAnnouncement


class AccountAdmin(UserAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = ('profile_picture_field', 'first_name', 'last_name', 'group', 'vk_profile_field')
    list_display_links = ('profile_picture_field', 'first_name')
    list_max_show_all = True
    list_filter = (('group', ChoiceDropdownFilter), )
    readonly_fields = ['profile_picture_field']

    def profile_picture_field(self, user: User):
        return format_html(user.get_profile_picture_tag())

    def vk_profile_field(self, user: User):
        return format_html(user.get_vk_link_tag())

    profile_picture_field.short_description = 'PFP'
    vk_profile_field.short_description = 'VK Profile'


class CustomAnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('header', 'object_content')
    search_fields = ('header', 'content')

    def object_content(self, obj: CustomAnnouncement) -> str:
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')


admin.site.register(User, AccountAdmin)
admin.site.register(CustomAnnouncement, CustomAnnouncementsAdmin)
