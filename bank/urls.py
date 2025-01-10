# This code snippet is defining URL patterns for a Django web application. It is using the `path`
# function from `django.urls` to map specific URL patterns to corresponding views in the application.
# Each `path` consists of a URL pattern, the view function that should be called when that URL is
# accessed, and a name for the URL pattern which can be used to refer to it in the code.

from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name='Homepage'),
    path("user/",views.User_profile,name="User"),
    path("edit/",views.edit_profile,name="Edit Profile"),
    path("dashbaord/",views.dashboard,name="Dashboard"),
    path("deposit/",views.deposit,name="Deposit"),
    path("Withdrawal/",views.withdrawal,name="WithDrawal"),
    path("transfer/",views.Transfer,name="Transfers"),
    path("loginpg/",views.loginpg,name="login page"),
    path("support/",views.support,name="support page"),
    path("transaction/",views.transaction,name="transaction page"),
    path("sign-up/",views.sign_up,name="Sign-up"),
    path("change-password/",views.change_password,name="Change Password"),
    path("Logout/",views.user_logout,name="Logout"),
]
