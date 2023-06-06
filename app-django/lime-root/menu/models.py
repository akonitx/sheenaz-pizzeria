from pprint import pprint as pp
from django.db.models import (
    Model,
    FloatField,
    ForeignKey,
    CharField,
    CASCADE,
    PositiveSmallIntegerField,
    PositiveIntegerField,
    TextField,
    ManyToManyField,
    RESTRICT,
    OneToOneField,
    DateTimeField,
    URLField,
    Value,
    Prefetch,
    Q,
)
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce


from django.urls import reverse


class Customer(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="customer")
    ua_phone_number = PositiveIntegerField(
        help_text="numbers starts after `+380`",
        unique=True,
        verbose_name="UA phone number",
    )
    session = CharField(max_length=400, null=True, blank=True)

    @property
    def num_of_orders(self):
        return self.orders.count()

    class Meta:
        ordering = ["ua_phone_number"]

    def __str__(self):
        return f"{self.user.username} {    self.user.email} +380{self.ua_phone_number} "


class Pizza(Model):
    SIZE_CHOICES = (
        (30, "30"),
        (50, "50"),
    )
    pizza_kind = ForeignKey(
        "PizzaKind",
        related_name="pizzas",
        on_delete=CASCADE,
    )
    size_cm = PositiveSmallIntegerField(choices=SIZE_CHOICES)
    weight_grams = PositiveSmallIntegerField()
    price_UAH = FloatField()

    class Meta:
        ordering = [
            "size_cm",
        ]

    def __str__(self):
        return f"|{self.pk}| {self.size_cm}, {round(self.price_UAH, ndigits=2)}"


class Topping(Model):
    name = CharField(max_length=120)
    price_UAH = FloatField()

    class Meta:
        ordering = ["pk", "name"]

    def __str__(self):
        return f"|{self.pk}| {str(self.name)}, {round(self.price_UAH, ndigits=2)}"


class Order(Model):
    customer = ForeignKey(
        Customer,
        on_delete=CASCADE,
        related_name="orders",
    )
    status = CharField(
        max_length=10,
        choices=[
            ("PROR", "pre-order"),
            ("INIT", "initialized"),
            ("DELV", "delivering"),
            ("FULF", "fulfilled"),
            ("CNCL", "canceled"),
        ],
    )
    publication_date = DateTimeField(auto_now_add=True)

    @staticmethod
    def evaluate_user_cost(queryset):
        """
        Evaluating cost for all pizzas and toppings in all OrderPizza, that relate to specific
        Order, which relate to specific Customer
        """
        total_cost = 0
        if queryset:
            for order in queryset:
                #
                total_cost += sum(
                    #  Getting OrderPizza amount
                    order_pizza.amount
                    * (
                        # Getting cost for pizza that customer added to OrderPizza
                        order_pizza.pizza.price_UAH
                        # Getting cost for toppings that customer added to OrderPizza
                        + sum(
                            topping.price_UAH for topping in order_pizza.toppings.all()
                        )
                    )
                    # Iterating through backward relationship from Order to PizzaOrder
                    for order_pizza in order.order_pizzas.all()
                )

        return total_cost

    def set_cost(self, value):
        setattr(self, "cost", value)

    @staticmethod
    def evaluate_cost(queryset):
        """
        Evaluating cost for all pizzas and toppings in all OrderPizza, that relate to specific
        Order
        """

        order_cost_dict = {}
        if queryset:
            for order in queryset:
                order_cost_dict[f"{order.pk}"] = sum(
                    #  Getting OrderPizza amount
                    order_pizza.amount
                    * (
                        # Getting cost for pizza that customer added to OrderPizza
                        order_pizza.pizza.price_UAH
                        # Getting cost for toppings that customer added to OrderPizza
                        + sum(
                            topping.price_UAH for topping in order_pizza.toppings.all()
                        )
                    )
                    # Iterating through backward relationship from Order to PizzaOrder
                    for order_pizza in order.order_pizzas.all()
                )

        return order_cost_dict

    @staticmethod
    def get_related_objects_for_admin():
        """
        Get related order objects (Pizza Order, Pizza, Toppings) to Order needed for
        represetning and prefetch them.

        For Order we need backward relationship with PizzaOrder.
        For PizzaOrder we need forward relationship with Pizza and Topping.
        """

        PizzaP = Prefetch("pizza", queryset=Pizza.objects.only("price_UAH"))
        ToppingsP = Prefetch("toppings", queryset=Topping.objects.only("price_UAH"))

        order_pizzas = Prefetch(
            "order_pizzas",
            # queryset=OrderPizza.objects.prefetch_related(PizzaP, ToppingsP),
            queryset=OrderPizza.objects.prefetch_related("pizza", "toppings"),
        )

        username = Prefetch(
            "customer",
            queryset=Customer.objects.defer("ua_phone_number").prefetch_related(
                Prefetch(
                    "user",
                    queryset=User.objects.only("username"),
                )
            ),
        )

        return Order.objects.prefetch_related(order_pizzas, username)

    @staticmethod
    def get_related_objects(customer_id=None):
        """
        Get all related order objects to current user needed for
        represetning and prefetch them.

        For Order we need backward relationship with PizzaOrder.
        For PizzaOrder we need forward relationship with Pizza and Topping.
        For Pizza we need forward relationship with PizzaKind.

        """

        # Checking to know if method is called for specific customer
        # (i.e. from OrderView.get()) or from AdminModel.get_queryset()
        customer_id = Q(customer=customer_id) if customer_id else Q()

        pizza_kind = Prefetch(
            "pizza_kind",
            queryset=PizzaKind.objects.defer("description"),
        )
        pizza = Prefetch(
            "pizza",
            queryset=Pizza.objects.prefetch_related(pizza_kind),
        )
        order_pizzas = Prefetch(
            "order_pizzas",
            queryset=OrderPizza.objects.prefetch_related(pizza).prefetch_related(
                "toppings"
            ),
        )

        return (
            Order.objects.prefetch_related(order_pizzas)
            .filter(customer_id)
            .defer("publication_date")
        )

    class Meta:
        ordering = ["publication_date"]

    def __str__(self):
        return f"{self.customer.user.username} {self.publication_date}"


class RepresentationFilling(Model):
    name = CharField(max_length=70, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class PizzaKind(Model):
    name = CharField(max_length=200)
    image_http_url = URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="HTTP URL to image",
    )
    representation_filling = ManyToManyField(RepresentationFilling)
    description = TextField(max_length=6000)

    def pizzas_srl(self):
        return self.prefetch_related("pizzas").pizzas

    def get_absolute_url(self):
        return reverse("pizza", kwargs={"pk": self.id})

    @property
    def load_all_sizes(self):
        pizzas = self.pizzas.all()

        self.all_sizes = {}
        for index, pizza in enumerate(pizzas, start=1):
            self.all_sizes[f"size{index}"] = {
                "pizza_id": pizza.pk,
                "size_cm": pizza.size_cm,
                "weight_grams": pizza.weight_grams,
                "price_UAH": int(pizza.price_UAH),
            }

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class OrderPizza(Model):
    order = ForeignKey(
        Order,
        on_delete=CASCADE,
        related_name="order_pizzas",
        null=True,
        blank=True,
    )
    pizza = ForeignKey(
        Pizza,
        on_delete=RESTRICT,
        related_name="orders",
    )
    toppings = ManyToManyField(
        Topping,
        blank=True,
        related_name="order_pizzas",
    )
    amount = PositiveSmallIntegerField(default=1)

    def set_amount(self, value):
        self.amount = value

    @staticmethod
    def get_all_related_objects():
        """
        Prefetch Pizza (which also prefetches PizzaKind) and Toppings
        """

        PizzaKindP = Prefetch("pizza_kind", PizzaKind.objects.only("name"))
        PizzaP = Prefetch(
            "pizza", Pizza.objects.only("price_UAH").prefetch_related(PizzaKindP)
        )
        ToppingsP = Prefetch("toppings", Topping.objects.only("price_UAH"))

        return OrderPizza.objects.prefetch_related(PizzaP, ToppingsP)

    @staticmethod
    def evaluate_cost(queryset):
        """
        Evaluating cost for all pizza and toppings
        """

        pizza_order_cost_dict = {}
        if queryset:
            for order_pizza in queryset:
                pizza_order_cost_dict[f"{order_pizza.pk}"] = (
                    #  Getting OrderPizza amount
                    order_pizza.amount
                    * (
                        # Getting cost for pizza that customer added to OrderPizza
                        order_pizza.pizza.price_UAH
                        # Getting cost for toppings that customer added to OrderPizza
                        + sum(
                            topping.price_UAH for topping in order_pizza.toppings.all()
                        )
                    )
                )

        return pizza_order_cost_dict

    class Meta:
        ordering = ["amount"]

    def __str__(self):
        return f"amount: {self.amount} pk:{self.pk}"
