# -*- coding: utf-8 -*-

from django.contrib import admin
from profiles.models import (
    Profile, ProfileForm, PhoneNumber, PhoneNumberForm, Email, EmailForm,
    SocialNetwork, SocialNetworkForm)


class PhoneNumberAdmin(admin.ModelAdmin):
    form = PhoneNumberForm
    list_display = ('number',)
    search_fields = ('number',)


class EmailAdmin(admin.ModelAdmin):
    form = EmailForm
    list_display = ('email',)
    search_fields = ('email',)


class SocialNetworkAdmin(admin.ModelAdmin):
    form = SocialNetworkForm
    list_display = ('network', 'link',)
    search_fields = ('network', 'link',)


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ('user', 'nick', 'birthday', 'note', 'gender',)
    search_fields = ('nick', 'birthday', 'note',)

admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(Profile, ProfileAdmin)
