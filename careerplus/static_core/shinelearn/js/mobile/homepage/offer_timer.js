
// Offer End date fetched from admin panel
const getnewDate = (date = null) =>
	!date
		? new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" }))
		: new Date(
			new Date(date).toLocaleString("en-US", { timeZone: "Asia/Kolkata" })
		);
const end_date = getnewDate("May 21, 2020 01:15:00").getTime();

//Function that will calculate the remaining day, hours, minutes, seconds

function timer_values(end_date){
    var now = getnewDate().getTime(); 
    var remaining_time = end_date - now; 
    var days = Math.floor(remaining_time / (1000 * 60 * 60 * 24)); 
    var hours = Math.floor((remaining_time%(1000 * 60 * 60 * 24))/(1000 * 60 * 60)); 
    var minutes = Math.floor((remaining_time % (1000 * 60 * 60)) / (1000 * 60)); 
    var seconds = Math.floor((remaining_time % (1000 * 60)) / 1000);
          
    return {
        days: days, 
        hours: hours,
        minutes: minutes,
        seconds: seconds
    }
}

function sticky_timer(days, hours, minutes, seconds){
    $('#sticky_timer_mobile').text(days + 'd : ' + hours + 'h : ' + minutes + 'm : ' + seconds + 's')
    return;
}

function popup_timer(days, hours, minutes, seconds){
    $('#days').text(days);
    $('#hours').text(hours);
    $('#min').text(minutes);
    $('#sec').text(seconds);
    return;
}

//when window loads, this function will trigger and it will calculate the days, hours, minutes and seconds
//and show on sticky and popup offer

$(window).ready(function(){
    const timer = setInterval(function() {
        var {days, hours, minutes, seconds} = timer_values(end_date)
        if(days < 0){
            clearInterval(timer);
            return;
        }
        sticky_timer(days, hours, minutes, seconds)
        popup_timer(days, hours, minutes, seconds)
        // if(($('body').attr('class'))){
        //     clearInterval(timer)
        // }
    }, 1000);

});