from menu.models import *
from random import randint

image_http_url = "https://s3.eu-central-1.amazonaws.com/lime-static-files.django/static/images/pizza.png"


fillings = [
    "Cheese",
    "Ham",
    "Pineapple" "Tomato sauce",
    "Pepperoni",
    "Olive oil",
    "Garlic",
    "Oregano",
    "Parmesan" "Mozzarella",
    "Basil leaves",
    "Italian sausage",
    "Mushrooms",
    "Onions",
    "Green peppers",
    "Black olives",
    "Ricotta",
]


pizza_kind = [
    {
        "name": "Margherita Pizza",
        "image_http_url": image_http_url,
        "description": "This classic pizza is made with a thin crust, tomato sauce, fresh mozzarella, and fresh basil. It originated in Naples, Italy, and is a simple yet delicious pizza that is loved by many.",
    },
    {
        "name": "Pepperoni Pizza",
        "image_http_url": image_http_url,
        "description": "This pizza is a staple in many American pizzerias and is made with a thin or thick crust, tomato sauce, mozzarella, and slices of spicy pepperoni sausage. It is a popular choice for meat lovers and is often served at parties and events",
    },
    {
        "name": "Hawaiian Pizza",
        "image_http_url": image_http_url,
        "description": "This controversial pizza is topped with tomato sauce, mozzarella, ham, and pineapple. It was created in Canada in the 1960s and has since become a popular pizza topping around the world. Some people love the sweet and salty combination of flavors, while others find the idea of putting fruit on a pizza to be sacrilegious.",
    },
    {
        "name": "Chicago Pizza",
        "image_http_url": image_http_url,
        "description": "Chicago-style pizza, also known as deep-dish pizza, is a pizza that originated in Chicago, Illinois. It is characterized by its thick, buttery crust that is baked in a deep dish and filled with, tomato sauce, and other toppings. Chicago-style pizza is a popular dish that has gained recognition worldwide and is often considered a symbol of Chicago's cuisine.",
    },
]

topping = {"meat": 20.5, "cheese": 14.25, "corn": 8.5, "salami": 15}

for i in pizza_kind:
    PizzaKind.objects.create(**i)
for i in topping:
    Topping.objects.create(name=f"{i}", price_UAH=topping[i])

pizza_kind = [
    PizzaKind.objects.get(id=1),
    PizzaKind.objects.get(id=2),
    PizzaKind.objects.get(id=3),
    PizzaKind.objects.get(id=4),
]

for i in fillings:
    RepresentationFilling.objects.create(name=i)

for i in range(1, 9):
    if i <= 4:
        size_cm = 30
        weight = 500 + randint(20, 101)
        price_UAH = 150 + size_cm + randint(0, 30)
        Pizza.objects.create(
            pizza_kind=pizza_kind[-1 + i],
            size_cm=size_cm,
            price_UAH=price_UAH,
            weight_grams=weight,
        )

    else:
        size_cm = 50
        weight = 900 + randint(20, 480)
        price_UAH = 150 + size_cm + randint(0, 30)
        Pizza.objects.create(
            pizza_kind=pizza_kind[-5 + i],
            size_cm=size_cm,
            price_UAH=price_UAH,
            weight_grams=weight,
        )
