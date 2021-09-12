from .views import snippet_list,register,checkuser,registerlogingoogleuser,login,verifyemail,checkgoogleuserexists,registergoogleuser,logingoogleuser,questionlist,addnewquestion,addnewresponse,getquestiondata,addlike,removelike,addresponselike,removeresponselike,getresponsedata,initiateresetpassword,forgotpasswordreset,submitnewpassword
from main.views import logoutMain
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', snippet_list,name='home'),
    path('accounts/register', register,name='register'),
    path('accounts/check-google-user-exists', checkgoogleuserexists,name='check-google-user-exists'),
    path('accounts/register-google-user', registergoogleuser,name='register-google-user'),
    path('accounts/login-google-user', logingoogleuser,name='login-google-user'),
    # path('login', obtain_auth_token,name='login'),
    path('accounts/login', login,name='login'),
    path('accounts/checkuser', checkuser,name='checkuser'),
    path('verify-email', verifyemail,name='verify-email'),
    path('logout-main', logoutMain, name="logout-main"),
    path('question-list/', questionlist, name='question-list'),
    path('initiate-password-reset/', initiateresetpassword, name='initiate-password-reset'),
    path('forgot-password-reset/', forgotpasswordreset, name='forgot-password-reset'),
    path('submit-new-password/', submitnewpassword, name='submit-new-password'),
    #################################################################
    path('add-new-question/', addnewquestion, name='add-new-question'),
    path('add-new-response/', addnewresponse, name='add-new-response'),
    path('get-question-data/', getquestiondata, name='get-question-data'),
    path('get-response-data/', getresponsedata, name='get-response-data'),
    ################################################################
    path('add-like/', addlike, name='add-like'),
    path('remove-like/', removelike, name='remove-like'),
    path('add-response-like/', addresponselike, name='add-response-like'),
    path('remove-response-like/', removeresponselike, name='remove-response-like'),
]