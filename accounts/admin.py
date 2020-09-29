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

class MachineAdmin(admin.ModelAdmin):
    list_display = ["Code","Name","Line","Page","Parameter","Address","Unit","LastEdit","Dev"]
    list_filter = ["Line","Page","Unit","Dev","Parameter"]
    search_fields = ["Line","Page","Code","Parameter","Address","Unit","LastEdit","Dev"]
    class Meta:
        model = MachineData

class LogDataAdmin(admin.ModelAdmin):
    list_display = ["id","DateCreated","Machine","Value"]
    list_filter = ["Machine"]
    search_fields = ["id","DateCreated","Machine","Value"]
    class Meta:
        model = LogData

class MessageAdmin(admin.ModelAdmin):
    list_display = ["msg","date_created","is_seen"]
    list_filter = ["is_seen"]
    class Meta:
        model = Message

admin.site.register(Account,AccountAdmin)
admin.site.register(MachineData,MachineAdmin)
admin.site.register(LogData,LogDataAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(IOTDev)
admin.site.register(UserAction,UserActionAdmin)


