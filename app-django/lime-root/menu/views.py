from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect


from json import loads

from Lime.settings import (
    SUCCESS_LOGIN_URL,
    SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL,
    LOGIN_URL,
    mainlog,
)
from menu.forms import *
from menu.models import PizzaKind, Topping, Customer, OrderPizza, Order, Pizza


class Pizzas(ListView):
    """Represents pizzakinds and pizzas for possibilities to add them to order"""

    #  prefeteching anothers models, to decrease ineficient amount of SQL queries
    #  We will need Filling and Pizza model for represent pizza as product, not a food
    queryset = PizzaKind.objects.prefetch_related("representation_filling", "pizzas")
    context_object_name = "pizza_kind_list"
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        #  Need to add Topping model to add user possibillities to add them to PizzaOrder model
        #  if user prefer
        context = super().get_context_data(**kwargs)

        #  Topping we need to represent them in template and combine them in OrderPizza instance
        context["toppings"] = Topping.objects.all()

        return context


class PizzaDetail(DetailView):
    """
    Represents pizzakind and pizzas for possibilities to add them to order but
    only one pizza kind with their all pizzas as product represantation (Pizza Model)
    """

    #  Need pizzas becauese pizzakind is only a pizza without size or price
    #  and pizza by itself is child of pizza kind with size and price attrs
    queryset = PizzaKind.objects.prefetch_related("pizzas")
    context_object_name = "pizzakind"
    template_name = "pizza_kind_detail.html"

    def get_context_data(self, **kwargs):
        #  Need to add Topping model to add user possibillities to add them to PizzaOrder model
        #  if user prefer
        context = super().get_context_data(**kwargs)

        #  Topping we need to represent them in template and combine them in OrderPizza instance
        context["toppings"] = Topping.objects.all()

        return context


class Registration(TemplateResponseMixin, FormMixin, ProcessFormView):
    """
    View for register(creating User, Customer instance) with forms for each Model(User and Instance)
    """

    template_name = "registration.html"
    success_url = reverse_lazy(SUCCESS_LOGIN_URL)
    form_class = UserCustomerRegistrationForm

    def form_valid(self, form):
        """
        If form is valid, then create User and Customer instance and relate them,
        and then login current registred user to requested session.
        """

        cd = form.cleaned_data

        user = User(
            username=cd["username"],
            first_name=cd["first_name"],
            last_name=cd["last_name"],
            email=cd["email"],
        )
        user.set_password(cd["password"])
        user.save()

        mainlog.info(f"{cd['username']} has set his first password")

        customer = Customer(ua_phone_number=cd["ua_phone_number"], user=user)
        customer.save()

        mainlog.info(f"{cd['username']} has set his firrst phonenumber")

        login(self.request, user=user)

        mainlog.info(f"{cd['username']} has been first loggined")

        return super().form_valid(form)


class Login(TemplateResponseMixin, FormMixin, ProcessFormView):
    template_name = "login.html"
    form_class = Login
    success_url = "/"

    def form_valid(self, form):
        """
        Checks user credentials, if fails, throw error, if good login
        """

        cd = form.cleaned_data

        user = authenticate(
            request=self.request, username=cd["username"], password=cd["password"]
        )
        if user is not None:
            login(request=self.request, user=user)

            mainlog.info(f"{cd['username']} has been logged in")

            return super().form_valid(form)
        else:
            form.add_error("password", "Inncorect entered password")

            mainlog.info(f"{cd['username']} has entered inncorect password to logg in")

            return super().form_invalid(form)


class Profile(
    LoginRequiredMixin,
    TemplateResponseMixin,
    FormMixin,
    ProcessFormView,
):
    """
    View that give accces user to change user first and last name
    """

    form_class = UserUpdateProfile
    template_name = "profile.html"
    success_url = SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL

    def get_profile(self):
        """
        Get user first and last name to populate the form with intial values
        """

        user = self.request.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    def get_initial(self):
        """
        populating intials to form
        """

        initial = super().get_initial()
        return initial | self.get_profile()

    def form_valid(self, form):
        """
        change first and last name id form valid
        """

        if form.has_changed():
            # We need to check if data from initials has been changed
            # If don't do this then user will submit same data as it is in DataBase
            # and it's will make ineficient queries

            # creating dict for use as value parameters for insertion to db
            user_values_to_insert = {
                db_field_name: form.cleaned_data[f"{db_field_name}"]
                # We need db_field_name in form.fields.keys() because
                # of it's mapping within Form fields and DB fields
                for db_field_name in form.fields.keys()
                if (db_field_name in form.changed_data)
            }
            User.objects.filter(pk=self.request.user.pk).update(**user_values_to_insert)

            first_name = (
                f"first name to {form.cleaned_data.get('first_name')}"
                if form.cleaned_data.get("first_name", None)
                else ""
            )
            last_name = (
                f" and last name to {form.cleaned_data.get('last_name')}"
                if form.cleaned_data.get("last_name", None)
                else ""
            )
            changed_attr = f"{first_name}{last_name}"
            mainlog.info(f"{self.request.user.username} has changed his {changed_attr}")

        return super().form_valid(form)


class ChangePassword(
    LoginRequiredMixin,
    TemplateResponseMixin,
    FormMixin,
    ProcessFormView,
):
    """
    View with password form to change its
    """

    form_class = ChangePassword
    template_name = "change_password.html"
    success_url = SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.request.user

        user.set_password(cd["password"])
        user.save()

        mainlog.info(f"{self.request.user.username} has changed his password")

        return super().form_valid(form)


class ChangePhoneNumber(
    LoginRequiredMixin,
    TemplateResponseMixin,
    FormMixin,
    ProcessFormView,
):
    """
    View with phone phone number to chnage its
    """

    form_class = ChangePhoneNumber
    template_name = "change_phone_number.html"
    success_url = SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL

    def get_initial(self):
        """
        Settings the user phone number as initials in form
        """

        initial = super().get_initial()
        return initial | {"ua_phone_number": self.request.user.customer.ua_phone_number}

    def form_valid(self, form):
        cd = form.cleaned_data
        customer = self.request.user.customer

        customer.ua_phone_number = cd["ua_phone_number"]

        customer.save()

        mainlog.info(
            f"{self.request.user.username} has changed his phone number to {cd['ua_phone_number']}"
        )

        return super().form_valid(form)


class ChangeUsername(
    LoginRequiredMixin,
    TemplateResponseMixin,
    FormMixin,
    ProcessFormView,
):
    """
    View for change the username
    """

    form_class = ChangeUsername
    template_name = "change_username.html"
    success_url = SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL

    def get_initial(self):
        """
        Settings the user username as initials in form
        """
        initial = super().get_initial()
        return initial | {"username": self.request.user.username}

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.request.user

        user.username = cd["username"]
        user.save()

        mainlog.info(
            f"{self.request.user.username} has changed his username to {cd['username']}"
        )

        return super().form_valid(form)


class ChangeEmail(
    LoginRequiredMixin,
    TemplateResponseMixin,
    FormMixin,
    ProcessFormView,
):
    """
    View for change the user email
    """

    form_class = ChangeEmail
    template_name = "change_email.html"
    success_url = SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL

    def get_initial(self):
        """
        Settings the user email as initials in form
        """

        initial = super().get_initial()
        return initial | {"email": self.request.user.email}

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.request.user

        user.email = cd["email"]
        user.save()

        mainlog.info(
            f"{self.request.user.username} has changed his email to {cd['email']}"
        )

        return super().form_valid(form)


class LogOut(
    LoginRequiredMixin,
    View,
    ContextMixin,
    TemplateResponseMixin,
):
    """
    View for logout user within it's request session
    """

    template_name = "logout.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def post(self, request):
        # need this var beacuse after user is logged out in request object
        # that we have user.username object does not exist
        # so we saved his username to use its in the log after logout() func
        # bellow will be called
        username = self.request.user.username

        logout(request=request)

        mainlog.info(f"{username} has loged out")

        return HttpResponseRedirect(SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL)


class OrderView(
    View,
    ContextMixin,
    TemplateResponseMixin,
):
    """
    View that represents all order that user has user
    """

    template_name = "order.html"

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(LOGIN_URL)
        context = {"orders": Order.get_related_objects(request.user.customer.pk)}

        mainlog.debug(
            "Order.get_related_objects(request.user.customer.pk) was added to context"
        )

        context["total_cost"] = Order.evaluate_user_cost(context["orders"])

        mainlog.debug("Order.evaluate_user_cost(context['orders'] was added to context")

        return render(request, "order.html", context=context)

    def _add_pizza(self, body, user, status="PROR"):
        """
        Add pizza with toppings or without toppings to OrderPizza and save it.
        Then add this OrderPizza to Order.
        Order is subsequently created when user creates OrderPizza.
        """

        pizza_order = OrderPizza()
        pizza_order.pizza_id = int(body["pizza_id"])
        pizza_order.save()

        mainlog.debug(
            f"{self.request.user.username} has created instance of OrderPizza and added Pizza with id: {body['pizza_id']} to its relationship"
        )

        pizza_order.order = Order.objects.create(customer=user.customer, status=status)

        mainlog.debug(
            f"{self.request.user.username} has created Order instance and added relation with that OrderPizza instance"
        )

        #  if body has toppings, then add toppinngs to OrderPizza
        if body.get("topping_ids", None):
            pizza_order.toppings.set(int(pk) for pk in body["topping_ids"])

            mainlog.debug(
                f"{self.request.user.username} has added toppings to his OrderPizza"
            )

        pizza_order.save()

    def post(self, request):
        """
        Method that handles creation of OrderPizza and add them to Order
        """

        body = loads(request.body)

        #   to add a new pizza to order the user must be auntheticated
        # and have pizza_id value to true
        if request.user.is_authenticated and body.get("pizza_id", None):
            # need to add relationship within customer(user) and order
            user = (
                User.objects.only("id")
                .select_related("customer")
                .get(username=request.user.username)
            )

            self._add_pizza(body=body, user=user)

            mainlog.info(f"{self.request.user.username} has created Order")

            response = {
                "fullfiled": True,
                "order_amount": request.user.customer.orders.count(),
            }

            return JsonResponse(response)

        else:
            response = {"not_authenticated": True, "redirect_login_url": LOGIN_URL}
            return JsonResponse(response)

    def _update_pizza_order_amount(self, dict):
        """
        Update OrderPizza amout of their instances specified in dict wiht mapping
        """

        #  OrderPizza instances that should to be updated
        order_pizzas = OrderPizza.objects.filter(pk__in=dict.keys()).only("pk")

        #  OrderPizza instances amount of which user changed.
        # key is id of OrderPizza and value is number of amount
        updated_value = {int(k): int(v) for k, v in dict.items()}

        # Update the amount values for each OrderPizza object
        for order_pizza in order_pizzas:
            # cheking if order_pizza.pk is in keys of updated_value
            if order_pizza.pk in updated_value:
                # if yes, then update this instance amount attr with value of this key
                # which is a value for amount attr
                order_pizza.amount = updated_value[order_pizza.pk]

                mainlog.info(
                    f"{self.request.user.username} has changed amount to {updated_value[order_pizza.pk]} in order Pizza with id: {order_pizza.pk}"
                )

        # Update the amount values in bulk
        OrderPizza.objects.bulk_update(order_pizzas, ["amount"])

    def _remove_toppings_relations(self, dict):
        """
        This method will use bulk delete to delete all relations
        beetween toppings and OrderPizza specified by user
        """

        # using this q_objects to save nested Q objects inside it
        q_objects = Q()
        for order_id, topping_ids in dict.items():
            q_objects |= Q(orderpizza_id=order_id, topping_id__in=topping_ids)

            mainlog.info(
                f"{self.request.user.username} has removed toppings with id-s: {', '.join(topping_ids)} on his Orders with id: {order_id}"
            )

        OrderPizza.toppings.through.objects.filter(q_objects).delete()

    def put(self, request):
        """
        Update amount attr in OrderPizza, delete toppings and Orders that user selected
        for deletion
        """

        #  Loading json, which will indicate which records to delete(topping and/or order)
        #  and which to update(amount in OrderPizza)
        body = loads(request.body)

        if body.get("submit", None) and request.user.is_authenticated:
            self._remove_toppings_relations(body.get("OrderPizzaID__ToppingsID", {}))

            if body["Order_id"]:
                Order.objects.filter(id__in=body["Order_id"]).delete()
                mainlog.info(
                    f"{self.request.user.username} has deleted Order with id-s: {', '.join(body['Order_id'])}"
                )

            # Checking if ChangePizzaOrderAmountID is not empty to don't make empty and ineficient queries
            if body.get("ChangePizzaOrderAmountID"):
                self._update_pizza_order_amount(dict=body.get("ChangePizzaOrderAmountID"))

            response = body
            request.user.customer.orders.filter(status="PROR").update(status="INIT")

            mainlog.info(
                f"{self.request.user.username} has added all his Orders to INIT status"
            )

            return JsonResponse(response)
        else:
            response = {"not_authenticated": True, "redirect_login_url": LOGIN_URL}
            return JsonResponse(response)
