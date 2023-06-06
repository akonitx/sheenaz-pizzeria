from pyexpat import model
from typing import Any
from django.contrib.admin import (
    ModelAdmin,
    display,
    register,
    StackedInline,
    TabularInline,
)


from menu.models import *
from django.core.paginator import Paginator
from django.core.cache import cache


# Modified version of a GIST I found in a SO thread
class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class OrderPizzaInline(TabularInline):
    model = OrderPizza
    extra = 0


class OrderInline(TabularInline):
    model = Order
    extra = 0


class PizzasInline(TabularInline):
    model = Pizza
    extra = 0


# Register your models here.
@register(PizzaKind)
class PizzaKindAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False
    inlines = [PizzasInline]
    list_display = ["name"]


@register(Topping)
class ToppingAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False
    list_display = ["name"]
    pass


@register(RepresentationFilling)
class RepresentationFilling(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False
    list_display = ["name"]


@register(Pizza)
class PizzaAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False

    @display(description="Name")
    def pizza_kind__name(obj):
        return f"{obj.pizza_kind.name}"

    list_select_related = ["pizza_kind"]
    list_display = [pizza_kind__name, "size_cm", "weight_grams", "price_UAH"]


@register(Customer)
class CustomerAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False

    @display(description="UserName")
    def user__username(obj):
        return obj.user.username

    @display(description="Email")
    def user__email(obj):
        return f"{obj.user.email}"

    list_select_related = ["user"]
    inlines = [OrderInline]
    list_display = [user__username, user__email, "ua_phone_number"]


@register(OrderPizza)
class OrderPizzaAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False

    def get_queryset(self, _reuqest):
        self.queryset = OrderPizza.get_all_related_objects()

        self.pizza_order_cost_dict = OrderPizza.evaluate_cost(self.queryset)

        return self.queryset

    @staticmethod
    @display(description="Pizza Name")
    def get_pizza_name(obj):
        #   obj = obj
        #   for i in self.queryset:
        #       if i.pk == obj.pk:
        #           obj = i

        return f"{obj.pizza.pizza_kind.name}"

    @display(description="Cost UAH")
    def cost(self, obj):
        cost = (
            self.pizza_order_cost_dict[f"{obj.pk}"]
            if str(obj.pk) in self.pizza_order_cost_dict
            else None
        )

        return cost

    list_display = [
        "pk",
        "get_pizza_name",
        "cost",
        "amount",
    ]


@register(Order)
class OrderAdmin(ModelAdmin):
    paginator = CachingPaginator
    show_full_result_count = False

    def get_queryset(self, _request):
        self.queryset = Order.get_related_objects_for_admin()

        self.order_cost_dict = Order.evaluate_cost(self.queryset)

        return self.queryset

    @display(description="Cost UAH")
    def cost(self, obj):
        cost = (
            self.order_cost_dict[f"{obj.pk}"]
            if str(obj.pk) in self.order_cost_dict
            else None
        )

        return cost

    @display(description="username")
    def customer__user__username(self, obj):
        return obj.customer.user.username

    inlines = [OrderPizzaInline]
    list_display = [
        "pk",
        "customer__user__username",
        "status",
        "publication_date",
        "cost",
    ]
