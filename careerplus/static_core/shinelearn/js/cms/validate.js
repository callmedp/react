if (window.CURRENT_FLAVOUR == 'mobile'){
    var highlightError = function(element, errorClass) {
        $(element).closest('.form-group').addClass('error');
        $(element).siblings('.mgs').show();
    };

    var unhighlightError = function(element, errorClass) {
        $(element).closest('.form-group').removeClass('error');
        $(element).siblings('.mgs').hide();
    };

    var errorPlacement = function(error, element){
        $(element).siblings('.mgs').html(error.text());
    };
    var showLeadForm = function () {
        // nothing
    };
}else{

    var highlightError = function(element, errorClass) {
        // $(element).siblings('.error').removeClass('hide_error');
        $(element).closest('.form-group').addClass('error');
    };

    var unhighlightError = function(element, errorClass) {
        // $(element).siblings('.error').addClass('hide_error');
        $(element).closest('.form-group').removeClass('error');
        $(element).siblings('.error-txt').html('');
    };

    var errorPlacement = function(error, element) {
        // $(element).siblings('.error').html(error.text());
        $(element).siblings('.error-txt').html(error.text());
    };

    var showLeadForm = function() {
        $('#id_download_model').modal("show");
    };
}

$('#callback_form').validate({
    rules: {
        name: {
            required: true,
            maxlength: 80
        },
        number: {
            required: true,
            number: true,
            minlength: 10,
            maxlength: 15
        },
        msg: {
            required: true,
            maxlength: 300
        }
    },
    messages: {
        name: {
            required: "Name is Mandatory.",
            maxlength: "Maximum 80 characters."
        },
        number: {
            required: "Mobile Number is Mandatory",
            number: "Enter only number",
            maxlength: "Please enter less than 16 digits",
            minlength: "Please enter atleast 10 digits"
        },
        msg: {
            required: "Message is required.",
            maxlength: "Enter less than 300 characters."
        }

    },
    highlight: function(element, errorClass) {
         $('#id_callback').removeAttr('disabled');
        // $(element).siblings('.error').removeClass('hide_error');
        $(element).closest('.form-group').addClass('error');
    },
    unhighlight: function(element, errorClass) {
        // $(element).siblings('.error').addClass('hide_error');
        $(element).closest('.form-group').removeClass('error');
        $(element).siblings('.error-txt').html('');
    },
    errorPlacement: function(error, element) {
        /*$(element).siblings('.error').html(error.text());*/
        $(element).siblings('.error-txt').html(error.text());
    }
});

$('#id_callback').click(function() {
    var $callbackForm = $("#callback_form");
        $('#id_callback').attr('disabled','true');
    var flag = $callbackForm.valid();
    if (flag) {
         if(document.getElementById('myModal' )){
     document.getElementById('myModal' ).style.display = 'none';
    }
        var formData = $callbackForm.serialize();
        $.ajax({
            url: "/lead/lead-management/",
            type: "POST",
            data: formData,
            success: function(data, textStatus, jqXHR) {
            pop('Your Query Submitted Successfully.');
            $('#id_callback').removeAttr('disabled');


                $('#callback_form')[0].reset();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                pop('Something went wrong. Try again later.');
                $('#id_callback').removeAttr('disabled');

            }
        });
    }

});


function pop(param) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerHTML=param;

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3500);
}