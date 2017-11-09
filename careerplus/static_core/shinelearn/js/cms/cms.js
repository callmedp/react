var highlightError = function(element, errorClass) {
    $(element).siblings('.error').removeClass('hide_error');
};

var unhighlightError = function(element, errorClass) {
    $(element).siblings('.error').addClass('hide_error');
};

var errorPlacement = function(error, element){
    $(element).siblings('.error').html(error.text());
};

var showLeadForm = function () {
    $('#id_download_model').modal("show");
};

$(document).ready(function() {

    $(document).on('click', '#id_download_button', function(event) {
        event.preventDefault();
        var pop_up = $(this).attr('pop-up');
        var href = $(this).attr('href');
        if (pop_up == "no") {
            $("#id_action").val(2);   // action for login -user
            $("#downloadpdf_form").submit();
            window.open(href, '_blank');
        }
        else {
            showLeadForm();
        }
    });

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $("input[name=country_code]").val(); //$('#call_back_country_code-id').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });

    var $pdfForm = $("#downloadpdf_form");
    $pdfForm.validate({

            rules:{
                name:{
                    required: true,
                    maxlength: 100
                },
                email:{
                    required: false,
                    maxlength: 100
                },
                mobile_number:{
                    required: true,
                    digits: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15,
                },
                term_condition:{
                    required: true
                }

            },
            messages:{
                name:{
                    required: "Name is mandatory",
                    maxlength: "Maximum 100 characters."
                },
                email:{
                    maxlength: "At most 100 characters"
                },
                mobile_number:{
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
            errorPlacement: errorPlacement
        });


    $(document).on('click', '#id_download', function(event) {
        // event.preventDefault();
        MyGA.SendEvent('QueryForm', 'Form Interactions', 'General Enquiry', 'success'); 
        $("#id_action").val(1);  //action on download button
        var $pdfForm = $("#downloadpdf_form");
        if ($pdfForm.valid()) {
            var href = $('#id_download_button').attr('href');
            $pdfForm.submit();
            $pdfForm[0].reset();
            $('#id_download_model').modal('toggle');
            window.open(href, '_blank');
        }
    });

    $("#id_skip").click(function(){
        MyGA.SendEvent('QueryForm', 'Form Interactions', 'General Enquiry', 'skip'); 
        var $pdfForm = $("#downloadpdf_form");
        $("#id_action").val(0);   // action on skip button
        $pdfForm.submit();
        // $pdfForm[0].reset();
        var href = $('#id_download_button').attr('href');
        window.open(href, '_blank'); 
    });

    $.validator.addMethod("custom_message",
        function(value, element) {
            if($('#id_message').val().trim()){
            
                return true;
            
            }
            return false;
    });

	$("#cms_comment_form").validate({
		rules: {
		    message: {
                required: true,
                custom_message: true,
                maxlength: 200
            }
		},
        messages:{
            message:{
                required: "Message is Mandatory.",
                maxlength: "Maximum 200 characters.",
                custom_message: "Message is Mandatory."
            }
        },
		highlight:function(element, errorClass) {
		        $(element).siblings('.error').removeClass('hide_error');
		},
		unhighlight:function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error'); 
		},
		errorPlacement: function(error, element){
		        $(element).siblings('.error').html(error.text());
		} 
    });

    $('#comment_submit').click(function() {
        var $commentForm = $("#cms_comment_form");
        var flag = $commentForm.valid();
        if (flag){
            var formData = $commentForm.serialize();
            var page_slug = $('#page_slug').val();
            var page_pk = $('#page_pk').val();
            $.ajax({
                url : "/cms/page/" + page_slug + "/" + page_pk + "/",
                type: "POST",
                data : formData,
                success: function(data, textStatus, jqXHR)
                {
                    $('#cms_comment_form')[0].reset();
                    alert('Thank you for sharing your opinion, your comment will be posted post moderation.');
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    alert('Something went wrong. Try again later.');
                }
            });
        }
    });




    $('#callback_form').validate({
        // submitHandler: function(form) {
        //     console.log("hii");
        //     var formData = $("#callback_form").serialize();
        //     console.log(formData);
        //     $.ajax({
        //         url : "/cms/lead-management/",
        //         type: "POST",
        //         data : formData,
        //         success: function(data, textStatus, jqXHR)
        //         {
        //             alert('Your Query Submitted Successfully.');
        //         },
        //         error: function (jqXHR, textStatus, errorThrown)
        //         {
        //             window.location.reload(); 
        //         }
        //     });  
        // },
        rules:{
            name:{
                required: true,
                maxlength: 80
            },
            mobile_number:{
                required: true,
                number: true,
                indiaMobile: true,
                minlength: 4,
                maxlength: 15
            },
            message_box:{
                required: true,
                maxlength: 300
            }
        },
        messages:{
            name:{
                required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters."
            },
            mobile_number:{
                required: "Mobile Number is Mandatory",
                number: "Enter only number",
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter less than 16 digits",
                minlength: "Please enter atleast 4 digits"
            },
            message_box:{
                required: "Message is required.",
                maxlength: "Enter less than 300 characters."
            }
            
        },
        highlight:function(element, errorClass) {
            $(element).siblings('.error').removeClass('hide_error'); 
        },
        unhighlight:function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error');    
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error').html(error.text());
        } 
    });

    $('#id_callback').click(function() {
        var $callbackForm = $("#callback_form");
        var flag = $callbackForm.valid();
        if (flag){
            var formData = $callbackForm.serialize();
            $.ajax({
                url : "/cms/lead-management/",
                type: "POST",
                data : formData,
                success: function(data, textStatus, jqXHR)
                {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Request Enquiry', 'success');
                    alert('Your Query Submitted Successfully.');
                    $('#callback_form')[0].reset();
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    MyGA.SendEvent('QueryForm', 'Form Interactions', 'Request Enquiry', 'Failure'); 
                    alert('Something went wrong. Try again later.');
                }
            });
        }
    });


    $(document).on('click', '#comment_load_more', function(event) {
        this.disabled = true;
        var formData = $("#loadform").serialize();
        $.ajax({
            url : "/ajax/page/load-more/",
            type: "POST",
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                data = JSON.parse(data);
                $("#total_comment").remove();
                $("#load_more").remove();
                $("#page_comment").append(data.comment_list);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
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

});
