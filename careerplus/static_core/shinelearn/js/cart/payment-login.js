$().ready(function() {

    $("#login_form").validate({
        rules: {
                email:{
                    required:true,
                    email:true
                },
                password:{
                    required:true,
                    minlength:6,
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