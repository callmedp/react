$(function(){

	$.validator.addMethod("indiaMobile", function(value, element) {
	    var country_code = $("select[name=country]").val(); //$('#call_back_country_code-id').val();
	    if (country_code == '91') {
	        return value.length == 10;
	    }
	    return true;
	});

	$('#pop_up_form').validate({
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
            },
            course: {
                required: true,
                minlength:1
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
            },
            course: {
                required: "Please select atleast one Course"
            }
        },
        highlight: function(element, errorClass) {
            $(element).closest('.form-group').addClass('error--mgs');
        },
        unhighlight: function(element, errorClass) {
            $(element).closest('.form-group').removeClass('error--mgs');
            $(element).siblings('.error--mgs').html('');
        },
        // errorPlacement: function(error, element) {
        //     $(element).siblings('.error--mgs').html(error.text());
        // }
    });

    $('#open-thanks').on('click', function(event) {
        event.preventDefault()
        var $availOfferForms = $("#pop_up_form");
        var flag = $availOfferForms.valid();
        if (flag) {
            var formData = $availOfferForms.serialize();
            $.ajax({
                url: "/lead/lead-management/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'success')
                    $("#thank-modal").addClass('show')
                    // $('#id_callback').removeAttr('disabled');
                    $("#pop_up_form").get(0).reset()

                },
                error: function(jqXHR, textStatus, errorThrown) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'Failure');
                    alert('Something went wrong. Try again later.');
                    $("#pop_up_form").get(0).reset()
                    // $('#id_callback').removeAttr('disabled');
                }
            });
        }
    
    });
});

