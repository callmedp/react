$().ready(function() {
    $("#register_form").validate({
        submitHandler: function(form) {     
        },
        rules: {
                name:{ required:true,},
                contact_number: { required:true,},
                email:{
                    required:true,
                    email:true
                },
                password1:{
                    required:true,
                    minlength:6,
                    maxlength: 10,
                },                
        },
        messages:{
            first_name:{ required:"Please enter username",},
            contact_number:{required:"Please provide 10 digit number"},
            email: { required:"Please enter a valid email address",},
            password1:{
                required: "Please provide a password",
            },
        },
        highlight:function(element, errorClass) {
                $(element).parent().addClass('error');
            },
        unhighlight:function(element, errorClass) {
                $(element).parent().removeClass('error');    
            },
        errorPlacement: function(error, element){
            
                // $(element).siblings('.js_id_error').html(error.text());
            } 
    });
});