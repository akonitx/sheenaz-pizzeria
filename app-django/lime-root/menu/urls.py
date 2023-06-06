from django.urls import path
from menu.views import (
    Pizzas,
    PizzaDetail,
    Registration,
    Login,
    Profile,
    ChangePassword,
    ChangePhoneNumber,
    ChangeUsername,
    ChangeEmail,
    LogOut,
    OrderView,
)

urlpatterns = [
    path("", Pizzas.as_view(), name="main-page"),
    path("pizza/<int:pk>/", PizzaDetail.as_view(), name="pizza"),
    path("register/", Registration.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("profile/", Profile.as_view(), name="profile"),
    path("change_password/", ChangePassword.as_view(), name="change-password"),
    path(
        "change_phone_number/", ChangePhoneNumber.as_view(), name="change-phone_number"
    ),
    path("change_username/", ChangeUsername.as_view(), name="change-username"),
    path("change_email/", ChangeEmail.as_view(), name="change-email"),
    path("logout/", LogOut.as_view(), name="logout"),
    path("order/", OrderView.as_view(), name="order"),
]
