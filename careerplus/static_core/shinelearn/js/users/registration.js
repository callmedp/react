$().ready(function() {
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
                    emailresponse = ( res.exists == false ) ? true : false;
                }
             });
             return emailresponse;

        },
        "This email id already taken."
    );

    $("#register_form").validate({
        submitHandler: function(form) {
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
                    uniqueUserName:true,
                },
                raw_password:{
                    required:true,
                    minlength:6,
                    maxlength: 15,
                },
                cell_phone:{
                    required:true,
                    number: true,
                    minlength: 10,
                    maxlength: 15,
                },
                term_conditions:{
                   required:true,
                },                
        },
        messages:{
            email: { 
                required:"Please enter a valid email address",                
            },
            raw_password:{
                required: "Please provide a password",
            },
            cell_phone:{
                required:"Mobile Number is Mandatory",
                number:"Enter only number",
                maxlength: "Please enter below 15 digits",
                minlength: "Please enter atleast 10 digits",
            },
            term_conditions:{
              required:"Please check term conditions",
            },
        },
    });
});
