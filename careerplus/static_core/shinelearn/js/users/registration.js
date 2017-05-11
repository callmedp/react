$().ready(function() {
    $("#register_form").validate({
        submitHandler: function(form) {
        $("#register_form").submit();     
        },
        rules: {
                email:{
                    required:true,
                    email:true
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
                // term_conditions:{
                //    required:true,
                // },                
        },
        messages:{
            email: { required:"Please enter a valid email address",},
            raw_password:{
                required: "Please provide a password",
            },
            cell_phone:{
                required:"Mobile Number is Mandatory",
                number:"Enter only number",
                maxlength: "Please enter below 15 digits",
                minlength: "Please enter atleast 10 digits",
            },
            // term_conditions:{
            //   required:"Please check term conditions",
            // },
        },
    });
});