$(document).ready(function () {
    $.validator.addMethod("lettersonly", function (value, element){
        return this.optional(element) || /^[a-z\s]*$/i.test(value);
    }, "Letters only please");

    $.validator.addMethod("defaultInvalid", function (value, element) {
        return !(element.value == element.defaultValue);
    }, "This field is required.");

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $('#id_country_code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });

    $("#lead").validate({
        submitHandler:function (form) {
            var action = $(form).attr('action');
            $.post(action, $(form).serialize(), function (data) {
                if (data && data['status']){
                    $.each($("#lead"), function (i, e) {
                        e.reset();
                    });
                    $("#lead label").remove();
                    alert('Thank you for your valuable suggestion.');
                    return false;
                }
            }, 'json');
        },
        rules:{
            number:{
                required:true,
                number:true,
                indiaMobile:true,
                minlength: 4,
                maxlength: 15,
            },
            name:{
                required:true,
                lettersonly:true,

            },
            msg:{
                required:true,
                maxlength:500,
            }
        },
        messages:{
            number:{
               required:"This field is required",
               indiaMobile: 'length must be 10 digits.',
               minlength: 'length must be greater than 3 digits.',
               maxlength: 'length must be less than 15 digits.',
            },
            name:{
                required:"This field is required"
            },
            msg:{
                required:"This field is required",
                maxlength:"No more than 500 characters."

            }
        },
        highlight: function(element) {
            $(element).closest('.form-group').addClass('error');
        },
        unhighlight: function(element) {
            $(element).closest('.form-group').removeClass('error');
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error-txt').html(error.text());
        }
    });
});
    