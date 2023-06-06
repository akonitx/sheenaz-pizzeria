function sussbstract_from_orders_cost(num) {
	let total_cost = document.querySelector('.cost');
	total_cost.innerHTML = Number(total_cost.innerHTML) - Number(num);
}

function parseCookie(str = document.cookie) {
	return str
		.split(';')
		.map(v => v.split('='))
		.reduce((acc, v) => {
			acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
			return acc;
		}, {});
}
function getRemoveOrderutton() {
	return document.querySelectorAll(".remove_from_order_button");
}

function getRemoveToppingFromPizzaOrderButton() {
	return document.querySelectorAll(".remove_topping_button");
}

function getIncrementAmountButton() {
	return document.querySelectorAll(".increment_button");
}
function getDecrementAmountButton() {
	return document.querySelectorAll(".decrement_button");
}

function get_submit_order_button() {
	return document.querySelector(".order_submit");
}

let remove_obj = { submit: true, OrderPizzaID__ToppingsID: {}, Order_id: [], ChangePizzaOrderAmountID: {} };

function removeOrder() {
	const removeOrderButtons = getRemoveOrderutton();
	removeOrderButtons.forEach((value) => {
		value.addEventListener("click", () => {

			let order_id = value.parentElement.dataset.orderId;
			let pizza_price = Number(value.parentElement.firstElementChild.firstElementChild.nextElementSibling.firstElementChild.nextElementSibling.firstElementChild.nextElementSibling.dataset.pizzaPrice);
			let pizzas_toppings_price = 0;



			let topping_li = value.parentElement.querySelector('li');

			if (topping_li !== null) {
				li_ele = topping_li.parentElement.querySelectorAll('li');
				for (li of li_ele) {
					pizzas_toppings_price += Number(li.dataset.toppingPrice);
				}
			}
			if (remove_obj.OrderPizzaID__ToppingsID.hasOwnProperty(order_id)) {
				delete remove_obj.OrderPizzaID__ToppingsID[`${order_id}`];
			}
			sussbstract_from_orders_cost((pizza_price + pizzas_toppings_price));
			remove_obj.Order_id.push(order_id);
			value.parentElement.remove();
		});
	});
}




function removeTopping() {
	let removeToppingList = getRemoveToppingFromPizzaOrderButton();
	removeToppingList.forEach((value) => {
		value.addEventListener("click", () => {
			order_el = value
				.parentElement
				.parentElement
				.parentElement
				.parentElement
				.parentElement
				.parentElement;



			if (typeof (remove_obj['OrderPizzaID__ToppingsID'][`${order_el.dataset.orderPizzaId}`]) === 'undefined') {
				remove_obj['OrderPizzaID__ToppingsID'][`${order_el.dataset.orderPizzaId}`] = [];
			}



			remove_obj['OrderPizzaID__ToppingsID'][`${order_el
				.dataset
				.orderPizzaId}`].push(value.parentElement.parentElement.dataset.toppingId);
			sussbstract_from_orders_cost(value.parentElement.parentElement.dataset.toppingPrice);

			value
				.parentElement
				.parentElement.remove();
		});

	});
}


removeTopping();

function getOrderPizzaAmount(value) {
	return value.parentElement.dataset.orderPizzaAmount;
}




function incrementAmount() {



	let incrementAmountButtons = getIncrementAmountButton();
	incrementAmountButtons.forEach((value) => {

		value.addEventListener('click', () => {
			value.previousElementSibling.innerHTML = Number(value.previousElementSibling.innerHTML) + 1;

			if (getOrderPizzaAmount(value) != value.previousElementSibling.innerHTML) {
				remove_obj.ChangePizzaOrderAmountID[`${value.parentElement.dataset.orderPizzaPk}`] = value.previousElementSibling.innerHTML;
			} else if (getOrderPizzaAmount(value) == value.previousElementSibling.innerHTML) {
				delete remove_obj.ChangePizzaOrderAmountID[`${value.parentElement.dataset.orderPizzaPk}`];
			};


		});

	});
}
function decrementAmount() {
	let decrementAmountButtons = getDecrementAmountButton();
	decrementAmountButtons.forEach((value) => {
		value.addEventListener('click', () => {

			if (value.nextElementSibling.innerHTML >= 2) {
				value.nextElementSibling.innerHTML = Number(value.nextElementSibling.innerHTML) - 1;
			}

			if (getOrderPizzaAmount(value) != value.nextElementSibling.innerHTML) {
				remove_obj.ChangePizzaOrderAmountID[`${value.parentElement.dataset.orderPizzaPk}`] = value.nextElementSibling.innerHTML;
			} else if (getOrderPizzaAmount(value) == value.nextElementSibling.innerHTML) {
				delete remove_obj.ChangePizzaOrderAmountID[`${value.parentElement.dataset.orderPizzaPk}`];
			};
		});

	});
}

removeOrder();
decrementAmount();
incrementAmount();





async function SubmitOrder() {
	let body = JSON.stringify(remove_obj);
	const post_order_request = new Request(`/order/`, {
		method: 'PUT',
		mode: 'same-origin',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': parseCookie(document.cookie).csrftoken,
		},
		body: body,
	}
	);
	await fetch(post_order_request);
	remove_obj.OrderPizzaID__ToppingsID = {};
	remove_obj.Order_id = [];
	remove_obj.ChangePizzaOrderAmountID = {};
	location.reload();


}


get_submit_order_button().addEventListener('click', SubmitOrder)




