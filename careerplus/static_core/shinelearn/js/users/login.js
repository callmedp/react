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
                    emailresponse = res.exists;
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
            }
            else
            {
                $('button[type="submit"]').prop('disabled', true);
            }   
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    emailDoesNotExist:true

                },
                password:{
                    required:true,
                    minlength:6,
                    maxlength: 15
                }
        },
        messages:{
            email: { required:"Please enter a valid email address"},
            password:{
                required: "Please provide a password"
            }
        }
    });   
});

$().ready(function() {
    $("#forgot_form").validate({
        submitHandler: function(form) {
            $.ajax({
                url: "",
                type: "POST",             
                data: new FormData($(form)),
                cache: false,             
                processData: false,      
                success: function(data){
                }
            });
        },
        rules: {
            email:{
                required:true,
                email:true,
            }
        },
        messages:{
            email: { required:"Please enter a valid email address"},
        }
    });
});
