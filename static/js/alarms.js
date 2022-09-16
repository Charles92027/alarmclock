

function loadAlarmsList() {
	
	const soundsTable = $('soundsTable');
	
	makeRequest({method: 'GET', url: '/alarms/'})
	.then((response) => {
	const alarms = JSON.parse(response);
		console.log(alarms);

		for (let index = 0; index < alarms.length; index++) {
			
			const alarm = alarms[index];
			console.log(alarm);
			
			let newRow = alarmsTable.insertRow(-1);

			let newCell = newRow.insertCell(0);
			let newAnchor = document.createElement("a");
			newAnchor.href = "/alarm/" + alarm.id
			let newText = document.createTextNode(alarm.id);
			newAnchor.appendChild(newText);
			newCell.appendChild(newAnchor);

			newCell = newRow.insertCell(1);
			newText = document.createTextNode(alarm.theTime);
			newCell.appendChild(newText);

			newCell = newRow.insertCell(2);
			newText = document.createTextNode(alarm.startDate);
			newCell.appendChild(newText);

			newCell = newRow.insertCell(3);
			newText = document.createTextNode(alarm.endDate);
			newCell.appendChild(newText);

			newCell = newRow.insertCell(4);
			newText = document.createTextNode(alarm.sound);
			newCell.appendChild(newText);

			newCell = newRow.insertCell(5);
			newText = document.createTextNode(alarm.enabled);
			newCell.appendChild(newText);
		}
		
		
		
	});
}

