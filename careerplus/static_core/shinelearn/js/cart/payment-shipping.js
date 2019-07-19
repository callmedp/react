$().ready(function() {


    $.validator.addMethod("indiaMobile", function(value, element) {
            var country_code = $('#id_country_code').val();
            if(country_code == '91'){
                return value.length == 10;
            }
            return true;
    });

    $.validator.addMethod("indiaPin", function(value, element) {
            var country_code = $('#id_country_code').val();
            if(country_code == '91'){
                return value.length == 6;
            }
            return true;
    });


    $("#guest_form").validate({
        // errorClass: 'error-txt',
        rules: {
                name:{
                    required: true,
                    maxlength: 60,
                },

                email:{
                    required: true,
                    email: true,
                    maxlength: 100,
                },
                mobile:{
                    required: true,
                    digits: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15,
                },
                country_code:{
                    required: true,
                },
                // address:{
                //     required: false,
                //     maxlength: 200,
                // },
                // pincode:{
                //     required: false,
                //     digits: true,
                //     indiaPin: false,
                // },
                // state:{
                //     required: false,
                //     maxlength: 100,
                // }
                      
        },
        messages:{
            name:{
                required: 'Name is required.',
                maxlength: 'length should be less than 60 characters',
            },
            email:{
                required: 'Email is required.',
                email: 'enter only valid email id',
                maxlength: 'length should be less than 100 characters',
            },

            
            mobile:{
                required: 'Contact is required.',
                digits: 'only digit accepted.',
                indiaMobile: 'length must be 10 digits.',
                minlength: 'length must be greater than 3 digits.',
                maxlength: 'length must be less than 15 digits.',
            },
            country_code:{
                required: 'this value is required.',
            },
            // address:{
            //     required: 'this value is required.',
            //     maxlength: 'length must be less than 200 characters.',
            // },
            // pincode:{
            //     required: 'this value is required.',
            //     digits: 'only digit accepted.',
            //     indiaPin: 'length must be 6 digits.',
            // },
            // state:{
            //     required: 'this value is required.',
            //     maxlength: 'length must be less than 200 characters.',
            // }
        },
        highlight: function(element) {

            /*if (window.CURRENT_FLAVOUR == 'mobile'){
                $(element).closest('.form-group').addClass('error');
            }
            else{
                $(element).closest('.col-sm-6').addClass('error');
            }*/

            var className = '.col-sm-6';
            if (window.CURRENT_FLAVOUR == 'mobile'){
                className = '.form-group';
            }
            $(element).closest('li').addClass('error');
        },
        unhighlight: function(element) {
            if (window.CURRENT_FLAVOUR == 'mobile'){
                $(element).closest('li').removeClass('error');
                $(element).siblings('.error--mgs').html('');

            }
            else{
                if ($(element).attr('name') != "country_code"){
                    $(element).closest('.col-sm-6').removeClass('error');
                }
            }
        },
        invalidHandler: function(event, validator) {
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error--mgs').html(error.text());
        }
    });

    $( "#id_country" ).change(function() {

        $.ajax({
            url: '/ajax/get-states/',
            type: 'GET',
            data: {"country": $( this ).val(), },
            dataType: 'json',
            success: function(json) {
                states = json.states;
                // initialize autocomplete with custom appendTo
                $('#id_state').autocomplete({
                    lookup: states
                });

            },
            failure: function(response){
                alert("Something went wrong, Please try again")
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again")
            }
        });

    });


    function init_autocomplete() {

        $.ajax({
            url: '/ajax/get-states/',
            type: 'GET',
            data: {"country": $('#id_country').val(), },
            dataType: 'json',
            success: function(json) {
                states = json.states;

                // initialize autocomplete with custom appendTo
                $('#id_state').autocomplete({
                    lookup: states
                });

            },
            failure: function(response){
                alert("Something went wrong, Please try again")
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again")
            }
        });        
    }

    init_autocomplete();


});
