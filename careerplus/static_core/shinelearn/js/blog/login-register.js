$().ready(function() {

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $('#id_country_code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });

    $("#login_form").validate({
        rules: {
                email:{
                    required:true,
                    email:true,
                    /*emailDoesNotExist:true,*/
                },
                password:{
                    required:true,
                    minlength:6,
                    maxlength: 15,
                },                
        },
        messages:{
            email: { required:"Please enter a valid email address",},
            password:{
                required: "Please provide a password",
            },
        },
    });

    $('#login-button').click(function() {
        flag = $("#login_form").valid();
        if (flag){
            var formData = $("#login_form").serialize();
            $('#login-button').prop('disabled', true);
            $.ajax({
                url : "/article/login-to-comment/",
                type: "POST",
                data : formData,
                success: function(data, textStatus, jqXHR)
                {
                    console.log(data);
                    if (data.response == 'login_user'){
                        window.location.reload();
                    }
                    else if (data.response == 'error_pass'){
                        var error_message = data.error_message;
                        $('#non-field-error').text(error_message)
                    }
                    else if (data.response == 'form_validation_error'){
                        $('#non-field-error').text('Please enter Valid Data')
                    }
                    $('#login-button').prop('disabled', false);
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    alert('Something went wrong. Try again later.');
                    $('#login-button').prop('disabled', false);
                }
            });
        }
    });


    $("#register_form").validate({
        rules: {
                email:{
                    required:true,
                    email:true
                },
                raw_password:{
                    required:true,
                    minlength:6,
                    maxlength: 15,
                },
                cell_phone:{
                    required:true,
                    number: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15,
                },
                term_conditions:{
                   required:true,
                },                
        },
        messages:{
            email: { required:"Please enter a valid email address",},
            raw_password:{
                required: "Please provide a password",
            },
            cell_phone:{
                required:"Mobile Number is Mandatory",
                number:"Enter only number",
                indiaMobile:"Length must be 10 digits.",
                maxlength: "Please enter less than 15 digits",
                minlength: "Please enter atleast 4 digits",
            },
            term_conditions:{
              required:"Please accept term conditions",
            },
        },
        errorPlacement: function(error, element) {
            if (element.attr("name") == "email")
            {
                error.appendTo("#user_email");
            }
            if (element.attr("name") == "raw_password")
            {
                error.appendTo("#raw_psd");
            }
            if (element.attr("name") == "cell_phone")
            {
                error.appendTo("#cell_phone");
            }
            if (element.attr("name") == "term_conditions")
            {
                error.appendTo("#terms");
            }
        }
    });

    $('#register-button').click(function() {
        flag = $("#register_form").valid();
        if (flag){
            $('#register-button').prop('disabled', true);
            var formData = $("#register_form").serialize();
            console.log(formData);
            $.ajax({
                url : "/article/register-to-comment/",
                type: "POST",
                data : formData,
                success: function(data, textStatus, jqXHR)
                {
                    if (data.response == 'login_user'){
                        window.location.reload();
                    }
                    else if (data.response == 'exist_user'){
                        $('#non-field-error-register').text(data.error_message)
                    }
                    else if (data.response == 'error_pass'){
                        $('#non-field-error-register').text(data.error_message)
                    }
                    else if(data.response == 'form_error'){
                        $('#non-field-error-register').text('Please enter Valid Data')
                    }
                    else if (data.response == 'form_validation_error'){
                        $('#non-field-error-register').text('Please enter Valid Data')
                    }
                    $('#register-button').prop('disabled', false);
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    alert('Something went wrong. Try again later.');
                    $('#register-button').prop('disabled', false);
                }
            });
        }
    });


});