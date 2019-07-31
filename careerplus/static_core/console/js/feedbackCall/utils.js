$(document).ready(function(){
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });
})


function formatDate(date,isTime) {
    let d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();
        hour = d.getHours();
        minutes = d.getMinutes();
        seconds = d.getSeconds();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;
    if (minutes>=0 && minutes<9) minutes = '0' + minutes;
    if (seconds>=0 && seconds<9) seconds ='0' + seconds;
    let resultDate = [year, month, day].join('-')
    if(isTime) 
        return `${resultDate} ${[hour,minutes,seconds].join(':')}`;
    return resultDate;
}