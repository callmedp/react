$(function(){
/*	var d = new Date($.now());
*/    $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd hh:ii:ss",
        autoclose: true,
        todayBtn: true,
        minuteStep: 5,
    });
});