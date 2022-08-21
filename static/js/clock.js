'use strict';




setInterval(() => {
    const d = new Date(); //object of date()
    const hr = d.getHours();
    const min = d.getMinutes();
    const sec = d.getSeconds();
    const hr_rotation = 30 * hr + min / 2; //converting current time
    const min_rotation = 6 * min;
    const sec_rotation = 6 * sec;
 
	const clockFace		= $('clockFace');
	const hourHand		= $('hourHand');
	const minuteHand	= $('minuteHand');
	const secondHand	= $('secondHand');
	
	if (hr >= 6 && hr < 18) {
		
		clockFace.classList.add("dayFace");
		clockFace.classList.remove("nightFace");

		hourHand.classList.add("dayHand");
		hourHand.classList.remove("nightHand");

		minuteHand.classList.add("dayHand");
		minuteHand.classList.remove("nightHand");

		secondHand.classList.add("dayHand");
		secondHand.classList.remove("nightHand");

	} else {
		
		clockFace.classList.add("nightFace");
		clockFace.classList.remove("dayFace");

		hourHand.classList.add("nightHand");
		hourHand.classList.remove("dayHand");

		minuteHand.classList.add("nightHand");
		minuteHand.classList.remove("dayHand");

		secondHand.classList.add("nightHand");
		secondHand.classList.remove("dayHand");
		
	}
  
    hourHand.style.transform = `rotate(${hr_rotation}deg)`;
    minuteHand.style.transform = `rotate(${min_rotation}deg)`;
    secondHand.style.transform = `rotate(${sec_rotation}deg)`;

}, 1000);

