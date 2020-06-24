$().ready(function() {

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $('#id_country_code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });

    $.validator.addMethod("pattern",
        function(value, element, regexp) {
            return this.optional(element) || regexp.test(value);
        },
        "Password must be the combination of alphanumeric, lowercase, uppercase and special character"
    );

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
                    emailresponse = !res.exists;
                }
            });
            return emailresponse;

        },
        "This email id is already taken."
    );

    $("#register_form").validate({
        submitHandler: function(form) {

            form.submit();    
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    uniqueUserName:true
                },
                raw_password:{
                    required:true,
                    minlength:8,
                    maxlength: 15,
                    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&].{7,15}$/
                },
                cell_phone:{
                    required:true,
                    number: true,
                    indiaMobile: true,
                    minlength: 6,
                    maxlength: 15
                },
                term_conditions:{
                    required:true
                },
        },
        messages:{
            email: { 
                required:"Please enter a valid email address"
            },
            raw_password:{
                required: "Please provide a password",
                minlength: "Password should be atleast 8 characters long!"
            },
            cell_phone:{
                required:"Mobile No. is mandatory",
                number:"Enter only numbers",
                indiaMobile: "Length must be 10 digits.",
                maxlength: "Please enter up to 15 digits",
                minlength: "Please enter at least 6 digits"
            },
            term_conditions:{
                required:"Please accept terms & conditions"
            },
        },
        highlight:function(element, errorClass) {
            $(element).closest('.form-group').addClass('error');
        },
        unhighlight:function(element, errorClass) {
            if ($(element).attr('name') != "country_code"){
                $(element).closest('.form-group').removeClass('error');
            }      
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error-txt').html(error.text());
        },
    });
});
