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


    $("#shipping_form").validate({
        rules: {
                first_name:{
                    required: true,
                    maxlength: 50,
                },
                last_name:{
                    required: true,
                    maxlength: 50,
                },
                // email:{
                //     required: true,
                //     email: true,
                //     maxlength: 100,

                // },
                mobile:{
                    required: true,
                    digits: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15,
                },
                address:{
                    required: true,
                    maxlength: 200, 
                },
                pincode:{
                    required: true,
                    digits: true,
                    indiaPin: true,
                },
                state:{
                    required: true,
                    maxlength: 100,
                }
                      
        },
        messages:{
            first_name:{
                required: 'this value is required.',
                maxlength: 'length should be less than 50 characters',
            },
            last_name:{
                required: 'this value is required.',
                maxlength: 'length should be less than 50 characters',
            },
            // email:{
            //     required: 'this value is required.',
            //     email: 'enter only valid email id',
            //     maxlength: 'length should be less than 100 characters',
            // },
            mobile:{
                required: 'this value is required.',
                digits: 'only digit accepted.',
                indiaMobile: 'length must be 10 digits.',
                minlength: 'length must be greater than 3 digits.',
                maxlength: 'length must be less than 15 digits.',
            },
            address:{
                required: 'this value is required.',
                maxlength: 'length must be less than 200 characters.',
            },
            pincode:{
                required: 'this value is required.',
                digits: 'only digit accepted.',
                indiaPin: 'length must be 6 digits.',
            },
            state:{
                required: 'this value is required.',
                maxlength: 'length must be less than 200 characters.',
            }
        },
    });

    $( "#id_country" ).change(function() {

        $.ajax({
            url: '/ajax/get-states/',
            type: 'GET',
            data: {"country_code": $( this ).val(), },
            dataType: 'json',
            success: function(json) {
                states = json.states;
                console.log(states);
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
            data: {"country_code": $('#id_country').val(), },
            dataType: 'json',
            success: function(json) {
                states = json.states;
                console.log(states);
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
