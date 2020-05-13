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
                minlength: 1
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
            $(element).closest('.form-group').addClass('error1');
        },
        unhighlight: function(element, errorClass) {
            if(element.type === 'checkbox'){
                $('#checkbox_error').html('')
            }
            else{
                $(element).closest('.form-group').removeClass('error1');
                $(element).siblings('.error-msg').html('');
            }
        },
        errorPlacement: function(error, element) {
            if(element.context.type === 'checkbox'){
                $('#checkbox_error').html(error.text())
            }
            else{
                $(element).siblings('.error-msg').html(error.text());
            }
        }
    });

    $('#avail_offer_id').on('click', function(event) {
        event.preventDefault()
        var $availOfferForm = $("#pop_up_form");
        var flag = $availOfferForm.valid();
        var selected_course = [];
        var extra_data = ""
        var msg = ""
        if (flag) { 
            $('#offerModal').modal('toggle')
            $.each($("input[name='course']:checked"), function(){
                selected_course.push($(this).val());
            })

            if(selected_course.length === 1){
                switch(selected_course[0].toLowerCase()){
                    case 'big data': {
                        extra_data = 'pop_bigdata'
                        break
                    }
                    case 'six sigma':{
                        extra_data = 'pop_sixsigma'
                        break
                    }
                    case 'cloud computing':{
                        extra_data = 'pop_cc'
                        break
                    }
                    case 'digital marketing':{
                        extra_data = 'pop_dm'
                        break
                    }
                    case 'data science':{
                        extra_data = 'pop_datascience'
                        break
                    }
                    default : extra_data = 'pop_others'
                }
            }
            else{
                extra_data = "pop_others"
                msg = selected_course.join(', ')
            }
            var formData = $availOfferForm.serialize()+ "&campaign=" + extra_data + "&msg=" + msg;
            $.ajax({
                url: "/lead/lead-management/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'success'); 
                    $('#thanksModal').modal('show')
                    $("#pop_up_form").get(0).reset()
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'Failure');
                    alert('Something went wrong. Try again later.');  
                    $("#pop_up_form").get(0).reset()
                }
            });
        }

    });
});

