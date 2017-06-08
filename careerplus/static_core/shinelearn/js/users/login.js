$().ready(function() {
    var emailresponse;
    $.validator.addMethod("emailDoesNotExist",
        function(value, element) {
            $.ajax({
                type: "GET",
                async: false,
                url:"/ajax/email-exist/",
                data:{email:$("#id_email").val()},
                success: function(res)
                {
                    emailresponse = ( res.exists == false ) ? false : true;
                }
             });
             return emailresponse;

        },
        "This email id does not exists."
    );
    $("#login_form").validate({
        submitHandler: function(form) {
            e.preventDefault();
            if($(this).val() != '')
            {
              $('button[type="submit"]').prop('disabled', false);  
              // $('button[type="submit"]').attr('disabled' , false); 
            }
            else
            {
                $('button[type="submit"]').prop('disabled', true);
              // $('button[type="submit"]').attr('disabled' , true);
            }   
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    emailDoesNotExist:true,

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
});