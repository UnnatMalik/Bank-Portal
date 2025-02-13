
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
    path("chatbot/",views.Chatbot,name="Chatbot")
]
