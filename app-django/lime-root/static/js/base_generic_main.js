function getFirstElementInTree(element) {
	return element.parentElement.firstElementChild;
}

function handleSizeClick(target, activeClass, inactiveClass) {
	if (!target.classList.contains("active")) {
		const active = getFirstElementInTree(target);
		const priceUah = target.parentElement.nextElementSibling;

		active.classList.remove(inactiveClass);
		active.classList.add(activeClass);

		const sibling = target.classList.contains('size_1')
			? target.nextElementSibling
			: target.previousElementSibling;

		sibling.classList.remove("active");
		target.classList.add("active");

		priceUah.innerText = `${target.dataset.pizzaPrice_uah} UAH`;
		priceUah.style.transform = 'scale(1.4)';
		priceUah.style.textShadow = "0 0 2px #fff, 0 0 10px #fff, 0 0 20px #FF6000, 0 0 30px #FF6000, 0 0 40px #FF6000, 0 0 50px #FF6000";
		setTimeout(() => {
			priceUah.style.transform = null;
			priceUah.style.textShadow = null;
		}, 400);
	}
}

function handleSize1Click(e) {
	handleSizeClick(e.target, 'background1', 'background2');
}

function handleSize2Click(e) {
	handleSizeClick(e.target, 'background2', 'background1');
}

document.querySelectorAll('.size_1').forEach((el) => {
	el.addEventListener('click', handleSize1Click);
});

document.querySelectorAll('.size_2').forEach((el) => {
	el.addEventListener('click', handleSize2Click);
});

function addTopping() {
	if (!this.classList.contains("active")) {
		this.classList.add("active");

		this.firstElementChild.style.display = "none";
		this.firstElementChild.nextElementSibling.style.display = "block";

		this.parentElement.classList.add("active");
	} else {
		this.classList.remove("active");

		this.firstElementChild.style.display = "block";
		this.firstElementChild.nextElementSibling.style.display = "none";

		this.parentElement.classList.remove("active");
	}

}

add_btns = document.querySelectorAll(".add_btn");
add_btns.forEach(ele => {
	ele.onclick = addTopping;
});

additionals = document.querySelectorAll(".additionals");

function showToppings() {
	if (!this.classList.contains('active')) {

		this.classList.add('active');
		this.parentElement.previousElementSibling.style.visibility = "visible";
		this.parentElement.previousElementSibling.style.opacity = "1";
	} else {

		this.classList.remove('active');
		this.parentElement.previousElementSibling.style.visibility = "collapse";
		this.parentElement.previousElementSibling.style.opacity = "0";
	}
}

additionals.forEach(ele => {
	ele.onclick = showToppings;
}
);


