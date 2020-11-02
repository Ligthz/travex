from django.urls import path

from django.contrib.auth import views as auth_views

from . import views, mobile



urlpatterns = [
    # Login Related
	path('premium-control-login/', views.loginPage, name="login"),  
	path('premium-control-logout/', views.logoutUser, name="logout"),

    # Indexes / Dashboard
    path('premium-control/', views.home, name="control-home"),
    path('premium-user-data/', views.data_landing, name="control-user"),
    path('user/', views.userPage, name="user-page"),
    path('account/<int:user_id>/', views.accountSettings, name="account"),

    # Information Details
    #path('machine/', views.machine, name="machine"),
    #path('data-landing/<datatype>/<line>', views.data_landing, name="data-landing"),
    #path('order_information/<int:pk>/', views.order_information, name="order_information"),

    
    # IOTCore
    #path('iot-core/', views.iotcore, name="iotcore"),

    # Mobile (User)
    path('', mobile.home, name="mobile-index"),
	path('mobile-login/', mobile.loginPage, name="mobile-login"),  
	path('mobile-logout/', mobile.logoutUser, name="mobile-logout"),
	path('mobile-register/', mobile.registerPage, name="mobile-register"),
    path('mobile-home/', mobile.home, name="mobile-home"),
    path('mobile-Portfolio/', mobile.Portfolio, name="mobile-Portfolio"),
    path('mobile-About_Traves/', mobile.About_Traves, name="mobile-About_Traves"),
    path('mobile-latest_news/', mobile.latest_news, name="mobile-latest_news"),
    path('mobile-account/', mobile.accountSettings, name="mobile-account"),

    # signup related
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/login/password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/login/password_reset_sent.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/login/password_reset_form.html"), 
        name="password_reset_confirm"),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/login/password_reset_done.html"), 
        name="password_reset_complete"),


]

handler404 = 'accounts.views.error_404_view'

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''