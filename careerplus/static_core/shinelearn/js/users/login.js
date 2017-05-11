$().ready(function() {
    $("#login_form").validate({
        submitHandler: function(form) {
            $("#login_form").submit();   
        },
        rules: {
                email:{
                    required:true,
                    email:true
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