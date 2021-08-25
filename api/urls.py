from .views import snippet_list,register,checkuser,registerlogingoogleuser,login,verifyemail,checkgoogleuserexists,registergoogleuser,logingoogleuser,questionlist
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
]