'use strict';

// dollar functions
// jquery is sooo heavy

function $(id) {return document.getElementById(id);}

function $hide(id) {
	$(id).classList.add("hidden");
}

function $show(id) {
	$(id).classList.remove("hidden");
}

function $disable(id) {
	$(id).disabled = true;
}

function $enable(id) {
	$(id).disabled = false;
}

function $listen(id, toWhat, how) {
	$(id).addEventListener(toWhat, how, true);
}

function $unlisten(id, toWhat, how) {
	$(id).removeEventListener(toWhat, how, true);
}

function makeRequest(options) {

	return new Promise(function (resolve, reject) {
  
		var request = new XMLHttpRequest();
		request.open(options.method, options.url);
		
		request.onload = function () {
		  
			if (request.status >= 200 && request.status < 300) {
				resolve(request.response);
			
			} else {
				reject({
					status: request.status,
					statusText: request.statusText
				});
			}
		};
		
		request.onerror = function () {
			reject({
				status: request.status,
				statusText: request.statusText
			});
		};
		
		if (options.headers) {
		
			Object.keys(options.headers).forEach(function (key) {
				request.setRequestHeader(key, options.headers[key]);
			});
		}
		
		var parameters = options.parameters;
		
		if (parameters && typeof parameters === 'object') {
			parameters = Object.keys(parameters).map(function (key) {
				return encodeURIComponent(key) + '=' + encodeURIComponent(parameters[key]);
			}).join('&');
		}
		request.send(parameters);
	});
}

/*

makeRequest({
	method: 'GET',
	url: 'http://example.com'
})
.then(function (response) {
	
})
.catch(function (err) {
	console.error('Augh, there was an error!', err.statusText);
});

*/