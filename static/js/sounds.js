

function loadSoundsList() {
	
	const soundsTable = $('soundsTable');
	
	makeRequest({method: 'GET', url: '/sounds/'})
	.then((response) => {
		
		const sounds = JSON.parse(response);
		console.log(sounds);

		for (let index = 0; index < sounds.length; index++) {
			
			const sound = sounds[index];
			console.log(sound);
			
			let newRow = soundsTable.insertRow(-1);
			let newCell = newRow.insertCell(0);
			
			let newSpan = document.createElement("span");
			newSpan.addEventListener('click', (event) => {
				playSound(event, sound);
			});
			
			let newText = document.createTextNode(sound);
			newSpan.appendChild(newText);
			newCell.appendChild(newSpan);
		}
		
		
		
	});
	//.catch(function (err) {
	//	console.error('Augh, there was an error!', err.statusText);
	//});

}


function playSound(event, sound) {
	
	console.log('playing: ' + sound);
	
	let url = '/sounds/' + sound + '/play/'
	
	makeRequest({method: 'GET', url: url})
	.then((response) => {
		// noop
	});

	
}