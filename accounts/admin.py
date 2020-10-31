from django.contrib import admin

# Register your models here.

from .models import *


class AccountAdmin(admin.ModelAdmin):
    list_display = ["username","name","phone","profile_pic","date_created","last_login"]
    list_filter = ["is_admin","is_staff","date_created"]
    search_fields = ["username","name"]
    class Meta:
        model = Account

class UserActionAdmin(admin.ModelAdmin):
    list_display = ["user","action","date_created"]
    list_filter = ["user"]
    search_fields = ["user","action"]
    class Meta:
        model = UserAction

class MessageAdmin(admin.ModelAdmin):
    list_display = ["msg","date_created","is_seen"]
    list_filter = ["is_seen"]
    class Meta:
        model = Message

admin.site.register(Account,AccountAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(UserAction,UserActionAdmin)


