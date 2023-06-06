function getOriginServerLink() {
	return document.querySelector("#origin_link").dataset['originLink'];

}
console.log(getOriginServerLink());

let OriginStatic = "https://s3.eu-central-1.amazonaws.com/lime-static-files.django/";
let OriginServer = getOriginServerLink();


var loader = document.querySelector('#preloader');
window.addEventListener('load', () => {
	loader.style.display = "none";

}
);


window.addEventListener("scroll", () => {

	if (window.scrollY > 95) {
		const logo = document.querySelector(".logo");
		const header = document.querySelector(".website_header");
		logo.style.transform = "scale(0.8)";

	} else if (window.scrollY < 95) {
		const logo = document.querySelector(".logo");
		logo.style.transform = "scale(1)";
	}
});

function change_box() {
	const pizza_box_counter = document.querySelector(".orders__number_orders");
	if (pizza_box_counter.innerText == 0) {
		pizza_box = document.querySelector(".pizza_box");
		pizza_box.src = `${OriginStatic}static/images/empty_pizza_box.png`;
	}
	else {
		pizza_box = document.querySelector(".pizza_box");
		pizza_box.src = `${OriginStatic}static/images/pizza_box.png`;
	}
};

window.addEventListener("load", change_box()
);
