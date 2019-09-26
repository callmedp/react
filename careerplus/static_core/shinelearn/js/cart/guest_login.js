$(document).ready(function () {
    var login_button = document.getElementById("login_guests")

    if (login_button != null) {
        login_button.addEventListener("click", guest_login);
    }

    async function guest_login() {
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r;
            i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date();
            a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
            a.async = 1;
            a.src = g;
            m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
        ga('create', 'UA-3537905-41', 'auto', { 'name': 'a' });
        ga('a.send', 'pageview');
        ga('create', 'UA-3537905-41', 'auto');
        ga('send', 'pageview');

        function hitGA() {
            ga('send', 'event', 'Cart Order Login', 'Buy Flow', 'Continue as Guest');
        }


        var form = document.getElementById('guest_form');
        const guest_info = $(form).serializeArray().reduce((obj, elem) => {
            obj[elem.name] = elem.value
            return obj;
        }, {})
        hitGA();
        let email = guest_info['email'] || '';
        let countryCode = guest_info['country_code'] || '';
        let mobile = guest_info['mobile'] || '';

        if ($('#guest_form').valid()) {

            // check mobile number valid 
            let isNumberValid = await numberValidate(countryCode, mobile);

            if(!isNumberValid){
                Swal.fire({
                    title: 'Error!',
                    text: `This number ${mobile} is not allowed with current country code ${countryCode}.`,
                    type: 'error',
                    showConfirmButton: false,
                    timer: 3500
                })
                return ;
            }


            // let isEmailRegistered = await checkEmailExists(email)
            // if (isEmailRegistered) {
            //     $('#email-error').html('This email already exists. Please register with some other email.');
            //     $('#email-error').closest('.form-group').addClass('error1');
            //     return;
            // }
            let input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "login_with");
            input.setAttribute("value", "login_guest")
            form.appendChild(input);
            form.submit();
        }


    }

    const numberValidate = async(countryCode, mobile) =>{
        // hit api to check whether the number with particular country is valid or not
        const resp = await fetch(`${site_domain}/api/v1/geolocation/validate/?country_code=${countryCode}&mobile=${mobile}`);
        const {result} = await resp.json();
        return result

    } 

    const checkEmailExists = async (email = '') => {
        //  create an api to check whether a user has registered email or not
        const result = await fetch(`${site_domain}/api/v1/cart/email-status/${email}/`)
        const { exists } = await result.json();
        return exists

    };

    $('#country_code').on('select2:select', function (e) {
        if($('#guest-mobile').val()){
            $('#guest-mobile').valid()
        }
    });
    /*
    * Fetch Country List
    * */
    const fetchCountryList = () => {
        $('#country_code').select2({
            placeholder: 'Search Country',
            ajax: {
                delay: 300,
                url: `${site_domain}/api/v1/geolocation/country/`,
                data: function (params) {
                    params.term = (params.term || '').trim()
                    params.term = params.term && params.term[0] === '+' ? params.term.substring(1) : params.term
                    let query = {
                        page: params.page || 1,
                        page_size: 10,
                        search: params.term
                    };
                    return query;
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.results.map(country => ({
                            id: country['phone'], text: `${country['name']}(+${country['phone']})`
                        })),
                        pagination: {
                            more: (params.page * 10) < data.count
                        }
                    };
                }
            },
            templateSelection: function (element) {
                return `+${element.id}`;
            },
            dropdownAutoWidth: true

        })
    };


    fetchCountryList();

    /*
     - auto fill the fields of the guest page, if the details of the user is available in the current cart. 
    */



    // auto fill the form if we have person details


    const autoFillGuestDetails = () => {

        let info = cartData.split(',');

        const formObj = {
            'name': info[0],
            'email': info[1],
            'country_code': info[2],
            'mobile': info[3]
        }
        document.forms['guest_form'].elements['name'].value = formObj['name'].trim() || ''
        if (formObj['name'].trim()) $("#guest_form input#guest-name").addClass('has-content');
        document.forms['guest_form'].elements['email'].value = formObj['email'].trim() || ''
        if (formObj['email'].trim()) $("#guest_form input#guest-email").addClass('has-content');
        const ccVal = formObj['country_code'] || '91';
        if ($('#country_code').find("option[value='" + ccVal + "']").length) {
            $('#country_code').val(ccVal).trigger('change');
        } else {
            // Create a DOM Option and pre-select by default
            var newOption = new Option(`+${ccVal}`, ccVal, true, true);
            // Append it to the select
            $('#country_code').append(newOption).trigger('change');
        }
        document.forms['guest_form'].elements['mobile'].value = formObj['mobile'].trim() || ''
        if (formObj['mobile'].trim()) $("#guest_form input#guest-mobile").addClass('has-content');

    }

    //  auto fill guest details 
    autoFillGuestDetails();




    jQuery.validator.addMethod("notEqualTo",
        function (value, element, param) {
            var notEqual = true;
            value = $.trim(value);
            for (i = 0; i < param.length; i++) {
                if (value == $.trim(param[i])) { notEqual = false; }
            }
            return this.optional(element) || notEqual;
        },
        "This number is not allowed."
    );


    jQuery.validator.addMethod("notStartWith",
        function (value, element, param) {
            var notEqual = true;
            value = $.trim(value);
            for (i = 0; i < param.length; i++) {
                if (value[0] == $.trim(param[i])) { notEqual = false; }
            }
            return this.optional(element) || notEqual;
        },
        "This number is not allowed." 
    );

    jQuery.validator.addMethod("minIndiaLengthValidator", 
    function (value, element, param) {
        if ($('#country_code').val() == '91'){
            value = $.trim(value);
            if(value.length <10)
            {
            return false;
            }

        }
       return true;
    },
     jQuery.validator.format("The length must be greater than 9 digits.")
);



    

    jQuery.validator.addMethod("maxIndiaLengthValidator", 
        function (value, element, param) {
            if ($('#country_code').val() == '91'){
                value = $.trim(value);
                if(value.length > 10 )
                {
                    return false;
                }

            }
           return true;
        },
         jQuery.validator.format("The length must be less than 11 digits.")
    );



    jQuery.validator.addMethod("maxOtherLengthValidator", 
        function (value, element, param) {
            if ($('#country_code').val() !== '91'){
                value = $.trim(value);
                if(value.length > 13 )
                {
                    return false;
                }

            }
            return true;
        },
         jQuery.validator.format("The length must be less than 14 digits.")
    );

    
    jQuery.validator.addMethod("minOtherLengthValidator", 
    function (value, element, param) {
        if ($('#country_code').val() !== '91'){
            value = $.trim(value);
            if(value.length  < 6 )
            {
                return false;
            }
        }
        return true;
    },
     jQuery.validator.format("The length must be greater than 5 digits.")
);




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

$.validator.addMethod("validateEmail", function(value, element) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(value);
},'Please provide a valid email id.');


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
                validateEmail: true,
                maxlength: 100,
            },
            mobile:{
                required: true,
                digits: true,
                indiaMobile: true,
                minIndiaLengthValidator: 10,
                maxIndiaLengthValidator: 10,
                minOtherLengthValidator: 6,
                maxOtherLengthValidator: 13,
                // minlength: 10,
                // maxlength: 10,
                notEqualTo: ['9999999999','8888888888', '9876543210',
                '7777777777', '9000000000', '8000000000',
                '9898989898',
                '6666666666'],
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
            digits: 'Only digit accepted.',
            indiaMobile: 'Length must be 10 digits.',
            minlength: 'Length must be 10 digits.',
            maxlength: 'Length must be 10 digits.',
            notEqualTo: 'This number is not allowed'
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

        let className = '.form-group', addClass = 'error1';

        if (window.CURRENT_FLAVOUR == 'mobile'){
            className = 'li';
            addClass = 'error'
        }
        $(element).closest(className).addClass(addClass);
    },
    unhighlight: function(element) {
        if (window.CURRENT_FLAVOUR == 'mobile'){
            $(element).closest('li').removeClass('error');
            $(element).siblings('.error--mgs').html('');

        }
        else{
             $(element).closest('.form-group').removeClass('error1');
             $(element).siblings('.error-txt').html('');
            // if ($(element).attr('name') != "country_code"){
            // }
        }
    },
    invalidHandler: function(event, validator) {
    },
    errorPlacement: function(error, element){

        let  errorTextClass = '.error-txt';
         if (window.CURRENT_FLAVOUR == 'mobile'){
           errorTextClass = '.error--mgs';
         }
         $(element).siblings(errorTextClass).html(error.text());
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




})
