from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('accounts/register-new', views.registerPageNew, name='register-new'),
    path('accounts/login-new', views.loginPageNew, name='login-new'),
    path('accounts/verify-email-success', views.verifyemailsuccess, name='verify-email-success'),
    path('accounts/verify-email-failed', views.verifyemailfailed, name='verify-email-failed'),
    path('accounts/verify-email-failed', views.verifyemailfailed, name='verify-email-failed'),
    path('accounts/forgot-password', views.forgotpassword, name='forgot-password'),
    path('accounts/confirm-new-password', views.confirmnewpassword, name='confirm-new-password'),
    path('accounts/password-reset-start-failed', views.passwordresetstartfailed, name='password-reset-start-failed'),
    path('accounts/confirm-new-password/<str:token>', views.confirmnewpassword, name='confirm-new-password'),
    ###############################################
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('', views.homePage, name='index'),
    path('new-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply'),
    ###########################################################
    path('accounts/user-profile/<str:username>', views.userprofile, name='user-profile'),
]
