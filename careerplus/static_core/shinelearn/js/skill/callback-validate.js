$(function(){

	$.validator.addMethod("indiaMobile", function(value, element) {
	    var country_code = $("select[name=country]").val(); //$('#call_back_country_code-id').val();
	    if (country_code == '91') {
	        return value.length == 10;
	    }
	    return true;
	});

	$('#id-request-callback-form').validate({
        rules: {
            name: {
                required: true,
                maxlength: 80
            },
            email: {
            	required: true,
            	maxlength: 100,
            	email: true,
            },
            number: {
                required: true,
                number: true,
                indiaMobile: true,
                minlength: 4,
                maxlength: 15
            }
        },
        messages: {
            name: {
                required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters."
            },
            email: {
                required: "Email is Mandatory.",
                maxlength: "Maximum 100 characters.",
                email: 'Please enter valid email.'
            },
            number: {
                required: "Mobile Number is Mandatory",
                number: "Enter only number",
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter atmost 15 digits",
                minlength: "Please enter atleast 4 digits"
            }
        },
        highlight: function(element, errorClass) {
            $(element).closest('.form-group').addClass('error');
        },
        unhighlight: function(element, errorClass) {
            $(element).closest('.form-group').removeClass('error');
            $(element).siblings('.error-txt').html('');
        },
        errorPlacement: function(error, element) {
            $(element).siblings('.error-txt').html(error.text());
        }
    });

    $('#request-callback-button').click(function() {
        var $callbackForm = $("#id-request-callback-form");
        var flag = $callbackForm.valid();
        if (flag) {
            var formData = $callbackForm.serialize();
            $.ajax({
                url: "/lead/lead-management/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Request Enquiry', 'success');
                    alert('Your Query Submitted Successfully.');
                    $('#id-request-callback-form')[0].reset();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Request Enquiry', 'Failure');
                    alert('Something went wrong. Try again later.');
                }
            });
        }
    });
});

