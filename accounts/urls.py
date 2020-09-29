from django.urls import path

from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    # Login Related
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    # Indexes / Dashboard
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    # Information Details
    path('machine/', views.machine, name="machine"),
    path('data-landing/<datatype>/<line>', views.data_landing, name="data-landing"),
    path('data-plot/<datatype>/<daytype>', views.data_plot, name="data-plot"),
    path('order_information/<int:pk>/', views.order_information, name="order_information"),

    
    # IOTCore
    path('iot-core/', views.iotcore, name="iotcore"),


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

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''