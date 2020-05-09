
// Offer End date fetched from admin panel
const end_date = new Date("5 10, 2020 12:52:25").getTime();

//Function that will calculate the remaining day, hours, minutes, seconds

function timer_values(end_date){
    var now = new Date().getTime(); 
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
    $('span#sticky_timer').text(days + 'd : ' + hours + 'h : ' + minutes + 'm : ' + seconds + 's')
    return;
}

function popup_timer(days, hours, minutes, seconds){
    $('.days').text(days);
    $('.hours').text(hours);
    $('.min').text(minutes);
    $('.sec').text(seconds);
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

    $('#avail_offer_id').on('click', function() {
        var $availOfferForm = $("#pop_up_form");
        var flag = $availOfferForm.valid();
        if (flag) {
            if(document.getElementById('offerModal' )){
                document.getElementById('offerModal' ).style.display = 'none';
            }
            var formData = $availOfferForm.serialize();
            console.log(formData)
            $.ajax({
                url: "/lead/lead-management/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    $('#thanksModal').modal('show')
                    $("#pop_up_form").get(0).reset()
                    // $('#id_callback').removeAttr('disabled');
                    // MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'success');
    
                    //     $('#callback_form')[0].reset();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    alert('Something went wrong. Try again later.');
                    $("#pop_up_form").get(0).reset()
                    // $('#id_callback').removeAttr('disabled');
                    // MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'Failure');
                }
            });
        }
    
    });
});

//When user click on Enroll Now, this function will trigger

// $('a#offer-timer').on('click', function(){
//     const timer = setInterval(function() { 
//         var {days, hours, minutes, seconds} = timer_values(end_date)

//         $('.days').text(days);
//         $('.hours').text(hours);
//         $('.min').text(minutes);
//         $('.sec').text(seconds);
        
//         if(!($('body').attr('class'))){
//             clearInterval(timer)
//         }
//     }, 1000);
// });