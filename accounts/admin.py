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

class UserTransactionsAdmin(admin.ModelAdmin):
    list_display = ["user","transaction","date_created"]
    list_filter = ["user"]
    search_fields = ["user","transaction"]
    class Meta:
        model = UserTransactions

class MessageAdmin(admin.ModelAdmin):
    list_display = ["msg","date_created","is_seen"]
    list_filter = ["is_seen"]
    class Meta:
        model = Message

class BlogAdmin(admin.ModelAdmin):
    list_display = ["author","date_created","body","image"]
    list_filter = ["author"]
    class Meta:
        model = Blog

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["average_profit","average_return_of_investment","total_investment_profit","total_investment_contra","total_investment_lost"]
    class Meta:
        model = Portfolio_data

class About_dataAdmin(admin.ModelAdmin):
    list_display = ["founded","header","topic1","body1","topic2","body2"]
    class Meta:
        model = About_data

admin.site.register(Account,AccountAdmin)
#admin.site.register(Message,MessageAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Portfolio_data,PortfolioAdmin)
admin.site.register(About_data,About_dataAdmin)
#admin.site.register(UserAction,UserActionAdmin)
admin.site.register(UserTransactions,UserTransactionsAdmin)


