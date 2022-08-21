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




