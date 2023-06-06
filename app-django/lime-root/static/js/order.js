function change_box_backgound(amount = 0) {
	const pizza_box_counter = document.querySelector(".orders__number_orders");

	if (amount == 0) {
		pizza_box_counter.innerText = amount;
		pizza_box = document.querySelector(".pizza_box");
		pizza_box.src = `${OriginStatic}static/images/empty_pizza_box.png`;
	}
	else {
		pizza_box_counter.innerText = amount;
		pizza_box = document.querySelector(".pizza_box");
		pizza_box.src = `${OriginStatic}static/images/pizza_box.png`;
	}
};


function parseCookie(str = document.cookie) {
	return str
		.split(';')
		.map(v => v.split('='))
		.reduce((acc, v) => {
			acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
			return acc;
		}, {});
}

function collect_active_items(val) {
	const actives = [];
	val.
		parentElement.
		parentElement.
		parentElement.querySelectorAll('.active').forEach((val) => { actives.push(val); });

	let acc = { pizza_id: null, topping_ids: [] };
	actives.map((val) => {

		if (Object.hasOwn(val.dataset, 'pizzaId')) {
			acc['pizza_id'] = val.dataset.pizzaId;
		}

		if (Object.hasOwn(val.dataset, 'toppingId')) {
			acc["topping_ids"].push(val.dataset.toppingId);
		}


	});
	return JSON.stringify(acc);
};


async function addNewOrder(request) {
	response = await fetch(request);
	return response;

}


async function handleClick(event) {
	const active_items = collect_active_items(event.target);
	const newOrderRequest = new Request(`/order/`, {
		method: 'POST',
		mode: 'same-origin',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': parseCookie(document.cookie).csrftoken,
		},
		body: active_items,
	}
	);
	const response = await addNewOrder(newOrderRequest);
	const response_json = await response.json();

	if (await response_json.not_authenticated) {
		window.location.replace(`${response_json.redirect_login_url}`);
	}
	else {
		change_box_backgound(await response_json.order_amount);
	}
}

const orders_button = document.querySelectorAll('.order');

orders_button.forEach((val) => {
	val.addEventListener('click', handleClick);
});


