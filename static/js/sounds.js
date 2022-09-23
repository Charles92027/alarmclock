
function playSound(sound) {
	
	console.log('playing: ' + sound);
	
	let url = '/sounds/' + sound + '/play'
	
	makeRequest({method: 'GET', url: url})
	.then((response) => {
		// noop
	});

	
}