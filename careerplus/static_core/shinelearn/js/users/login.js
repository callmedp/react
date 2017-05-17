$().ready(function() {
    $.validator.addMethod("email_account", function(value, element) {
        $.get("/ajax/email-exist/", {email:$("#id_email").val() }, function(msg){
           {
              if(msg.exists == "false")
                 return false;  
              return true;
           }
        })}, "User have No account");
    $("#login_form").validate({
        submitHandler: function(form) {
            $("#login_form").submit();   
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    email_account:$("#id_email").val()

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