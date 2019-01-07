$().ready(function() {
$('#login_form').on('submit', function() {
 hitGAContinue();
});

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
                required: "Please enter valid password",
            },
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
