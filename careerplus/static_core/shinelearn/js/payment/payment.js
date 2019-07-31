$(document).ready(function () {
    $('#check-sumit-button').click(function () {
        if ($('#check-pay-form').valid()) {
            $('#check-pay-form').submit();
        }
    });

    $.validator.addMethod("validState", function (value, element) {
        var state_id = $('#id_state').val();
        if (state_id != -1) {
            return true;
        }
        return false;
    });

    $("#id-cash-form").validate({
        rules: {
            state: {
                required: true,
                validState: true,
            },
        },
        messages: {
            state: {
                required: 'this value is required.',
                validState: 'Please select valid state.',
            },
        },
    });

    var today = new Date();
    // set end date to max one year period:
    var start = new Date(new Date().setMonth(today.getMonth() - 3));

    var end = new Date(new Date().setYear(today.getFullYear() + 1));


    $('#id_deposit_date').datepicker({
        startDate: start,
        endDate: end,
        format: "dd-mm-yyyy",
        weekStart: 1,
        orientation: "bottom left",
        daysOfWeekHighlighted: "1,2,3,4,5,6",
        autoclose: true,
        todayHighlight: true
    });

    $("#check-pay-form").validate({
        rules: {
            cheque_no: {
                required: true,
                digits: true,
                minlength: 6,
                maxlength: 6,
            },
            drawn_bank: {
                required: true,
            },
            deposit_date: {
                required: true,
            },
        },
        messages: {
            cheque_no: {
                required: 'this field is required.',
                digits: 'enter only digits.',
                minlength: 'length must be 6 digits.',
                maxlength: 'length must be 6 digits.',
            },
            drawn_bank: {
                required: 'this field is required.',
            },
            deposit_date: {
                required: 'this field is required.',
            },
        },
        highlight: function (element, errorClass) {
            let className = '.form-group', addClass = 'error1';

            $(element).closest(className).addClass(addClass);
        },
        unhighlight: function (element, errorClass) {
            let className = '.form-group', removeClass = 'error1', errorTextClass = '.error-txt';

            $(element).closest(className).removeClass(removeClass);
            $(element).siblings(errorTextClass).html('');
        },
        errorPlacement: function (error, element) {
            let  errorTextClass = '.error-txt';
            $(element).siblings(errorTextClass).html(error.text());

        },

    });


});