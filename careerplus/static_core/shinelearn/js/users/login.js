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
            // e.preventDefault();
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
            var formData = $(form).serialize();
            var post_url = $(form).attr('action' );
            $('#forgot_div').modal('hide');
            $.ajax({
                url: post_url,
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(json) {
                    $("#forgot_form")[0].reset();
                    if (json.exist == true){
                        alert("Link has been sent to your registered email id");
                    }
                    else if (json.notexist == true){
                        alert("your email does not exist on shine learning");
                    }
                    else if (json.noresponse == true){
                        alert("Something went wrong. Try again later");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
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
