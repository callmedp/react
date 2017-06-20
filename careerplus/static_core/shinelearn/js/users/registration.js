$().ready(function() {

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $('#id_country_code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });

    var emailresponse;
    $.validator.addMethod("uniqueUserName",
        function(value, element) {
            $.ajax({
                type: "GET",
                async: false,
                url:"/ajax/email-exist/",
                data:{email:$("#id_email").val()},
                success: function(res)
                {
                    emailresponse = !res.exists;
                }
            });
            return emailresponse;

        },
        "This email id already taken."
    );

    $("#register_form").validate({
        submitHandler: function(form) {
            e.preventDefault();
            if($(this).val() != '')
                {
                    $('button[type="submit"]').attr('disabled' , false); 
                }
            else
                {
                    $('button[type="submit"]').attr('disabled' , true);
                }     
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    uniqueUserName:true
                },
                raw_password:{
                    required:true,
                    minlength:6,
                    maxlength: 15
                },
                cell_phone:{
                    required:true,
                    number: true,
                    indiaMobile: true,
                    minlength: 6,
                    maxlength: 15
                },
                hello: {
                    required: true
                },
                term_conditions:{
                    required:true
                }
        },
        messages:{
            email: { 
                required:"Please enter a valid email address"
            },
            raw_password:{
                required: "Please provide a password"
            },
            cell_phone:{
                required:"Mobile No. is mandatory",
                number:"Enter only numbers",
                indiaMobile: "Length must be 10 digits.",
                maxlength: "Please enter up to 15 digits",
                minlength: "Please enter at least 6 digits"
            },
            term_conditions:{
                required:"Please check terms & conditions"
            }
        }
    });
});
