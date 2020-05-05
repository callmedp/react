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

$.validator.addMethod("indiaMobile", function(value, element) {
    var country_code = $("input[name=country]").val(); //$('#call_back_country_code-id').val();
    if (country_code == '91') {
        return value.length == 10;
    }
    return true;
});

$.validator.addMethod("custom_message",
    function(value, element) {
        if ($('#id_message').val().trim()) {

            return true;

        }
        return false;
    });

$(document).on('click', '#id_download_button', function(event) {
    event.preventDefault();
    var pop_up = $(this).data('popup');
    var href = $(this).attr('href');
    if (pop_up == "no") {
        // $("#id_action").val(2); // action for login -user
        $.ajax({
            url: "/lead/lead-management/",
            type: "POST",
            data: $("#downloadpdf_form").serialize(),
            success: function(data, textStatus, jqXHR) {
                MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Resume Enquiry', 'success');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Resume Enquiry', 'Failure');
                alert('Something went wrong. Try again later.');
            }
        });
        if (window.CURRENT_FLAVOUR == 'mobile'){
            $('.cls_mask').click(); 
        }
        window.open(href, '_blank');
    } else {
        showLeadForm();
    }
});

    // event.preventDefault();

    // var $pdfForm = $("#downloadpdf_form");
    $('form#downloadpdf_form').each(function(ele){
        $(this).validate({
            rules: {
                name: {
                    required: true,
                    maxlength: 100
                },
                email: {
                    required: false,
                    maxlength: 100
                },
                number: {
                    required: true,
                    digits: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15,
                },
                term_condition: {
                    required: true
                }
    
            },
            messages: {
                name: {
                    required: "Name is mandatory",
                    maxlength: "Maximum 100 characters."
                },
                email: {
                    maxlength: "At most 100 characters"
                },
                number: {
                    required: "Mobile Number is Mandatory",
                    digits: "Enter only digits",
                    indiaMobile: "Please enter 10 digits only",
                    minlength: "Please enter atleast 4 digits",
                    maxlength: "Please enter less than 16 digits",
    
                },
                term_condition: {
                    required: "Please accept our Terms & Conditions"
                }
    
            },
            highlight: highlightError,
            unhighlight: unhighlightError,
            errorPlacement: errorPlacement,
            submitHandler: function(form){
    //            MyGA.SendEvent('QueryForm', 'Form Interactions', 'General Enquiry', 'success');
                // $("#id_action").val(1); //action on download button
    
                var formData = $(form).serialize();
                $.ajax({
                    url: "/lead/lead-management/",
                    type: "POST",
                    data: formData,
                    success: function(data, textStatus, jqXHR) {
                        MyGA.SendEvent('QueryForm', 'Form Interactions', 'CMS Resume Enquiry', 'success');
                        // alert('Your Query Submitted Successfully.');
                        if (window.CURRENT_FLAVOUR == 'mobile'){
                            $('.cls_mask').click();
                            $("#downloadpdf_form").get(0).reset()
                            var href = $('a#id_download_button').get(ele).href;
                            window.open(href, '_blank');  
                        }
                        else{
                            // $pdfForm.reset();
                            $("#downloadpdf_form").get(0).reset()
                            var href = $('a#id_download_button').get(ele).href;
                            $('#id_download_model').modal('toggle');
                            window.open(href, '_blank');
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        MyGA.SendEvent('QueryForm', 'Form Interactions', 'CMS Resume Enquiry ', 'Failure');
                        alert('Something went wrong. Try again later.');
                    }
                });
                return false;
            }
        })
    });


$(document).on('click', '#comment_load_more', function(event) {
    this.disabled = true;
    var formData = $("#loadform").serialize();
    $.ajax({
        url: "/ajax/page/load-more/",
        type: "POST",
        data: formData,
        success: function(data, textStatus, jqXHR) {
            data = JSON.parse(data);
            $("#total_comment").remove();
            $("#load_more").remove();
            $("#page_comment").append(data.comment_list);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Can't load more comments.");
        }
    });
});


$(document).on('click', '#cms_share', function(event) {
    $.ajax({
        url: "/ajax/page/cms-share/",
        type: 'GET',
        data: {
            page_id: $(this).attr('page-id')
        },
        success: function(data) {
            console.log('success');
        }
    });

});


$(function() {
    $("a#id_skip").each(function(ele){
        $(this).click(function() {
            MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Resume Enquiry', 'skip');
            if (window.CURRENT_FLAVOUR == 'mobile'){
                $('.cls_mask').click(); 
            }
            var href = $('a#id_download_button').get(ele).href;
            window.open(href, '_blank');
        })
    });

    $('.toggle-index').click(function(){
        $('.display-more-index').toggle();
        $('.toggle-index').html($('.toggle-index').text() == 'View less' ? 'View all' : 'View less');
    });

    $("#cms_comment_form").validate({
        rules: {
            message: {
                required: true,
                custom_message: true,
                maxlength: 200
            }
        },
        messages: {
            message: {
                required: "Message is Mandatory.",
                maxlength: "Maximum 200 characters.",
                custom_message: "Message is Mandatory."
            }
        },
        highlight: function(element, errorClass) {
            $(element).siblings('.error').removeClass('hide_error');
        },
        unhighlight: function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error');
        },
        errorPlacement: function(error, element) {
            $(element).siblings('.error').html(error.text());
        },
        submitHandler: function(form) {
            var formData = $(form).serialize();
            var page_slug = $('#page_slug').val();
            var page_pk = $('#page_pk').val();
            $.ajax({
                url: "/cms/page/" + page_slug + "/" + page_pk + "/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    $('#cms_comment_form')[0].reset();
                    alert('Thank you for sharing your opinion, your comment will be posted post moderation.');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    alert('Something went wrong. Try again later.');
                }
            });
        }
    });


    $('#callback_form').validate({
        rules: {
            name: {
                required: true,
                maxlength: 80
            },
            number: {
                required: true,
                number: true,
                indiaMobile: true,
                minlength: 4,
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
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter less than 16 digits",
                minlength: "Please enter atleast 4 digits"
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
            var formData = $callbackForm.serialize();
            $.ajax({
                url: "/lead/lead-management/",
                type: "POST",
                data: formData,
                success: function(data, textStatus, jqXHR) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'success');
                    alert('Your Query Submitted Successfully.');
                        $('#id_callback').removeAttr('disabled');

                    $('#callback_form')[0].reset();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Enquiry', 'Failure');
                    alert('Something went wrong. Try again later.');
                                                $('#id_callback').removeAttr('disabled');

                }
            });
        }
    });



});

      $(document).on('click', '.icon-downlod', function () {

    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Cms Resume Enquiry', 'success');
});