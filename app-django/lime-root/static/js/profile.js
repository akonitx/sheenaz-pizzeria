const log_out = document.querySelector(".log_out");

const log_out_json = JSON.stringify({ log_out: true });


function parseCookie(str = document.cookie) {
	return str
		.split(';')
		.map(v => v.split('='))
		.reduce((acc, v) => {
			acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
			return acc;
		}, {});
}


const log_out_req = new Request(`/logout/`, {
	method: 'POST',
	mode: 'same-origin',
	headers: {
		'Content-Type': 'application/json',
		'X-CSRFToken': parseCookie(document.cookie).csrftoken,
	},
	body: log_out_json,
}
);



log_out.addEventListener('click', async () => {
	await fetch(log_out_req);
	window.location.replace('/');
});



