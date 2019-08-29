function viewDetailOrderitem(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/dashboard/inbox-detail/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
                window.scrollTo(0, 0);
               // $("#load_more" + article_id).remove();
               // $("#page_comment" + article_id).append(html);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        });
    }
};

function viewCommentOrderitem(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/dashboard/inbox-comment/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
                window.scrollTo(0, 0);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        });
    }
};

function giveFeedbackOrderitem(oi_pk,rating) {

    if (oi_pk){
        $.ajax({
            url: '/dashboard/inbox-feedback/',
            type: "GET",
            data : {'oi_pk': oi_pk, 'rating':rating},
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
                window.scrollTo(0, 0);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                if (xhr.status == 400){
                    return;
                }
                alert("Something went wrong, try after sometimes.");
            }
        });
    }
};

function rejectService(oi_pk) {
    $("#reject-modal" + oi_pk).modal("show");
    $(document).on('click', '#reject-submit-button' + oi_pk, function () {
        $("#reject-form-id" + oi_pk).validate({
            rules: {
                comment:{
                    required: function(){
                        if($('#reject-file-id').val() == "")
                            return true;
                        else
                            return false;
                    },
                },

                reject_file: {
                    extn: true,
                }
            },

            messages: {
                comment: 'This field is required',
                reject_file: 'only pdf, doc and docx formats are allowed',
            },

            highlight: function(element) {
                $(element).closest('.form-group').addClass('error')
            },
            unhighlight: function(element) {
                $(element).closest('.form-group').removeClass('error')
            },
            errorPlacement: function(error, element){
                $(element).closest('.form-group').find(".error-txt").html(error.text());
            },
            
            submitHandler: function(form) {                
                return false;
            },

        });

        var flag = $('#reject-form-id' + oi_pk).valid();
        if (flag){
            var formData = new FormData($('#reject-form-id' + oi_pk)[0]);
            console.log($('#reject-reason').val());
            $.ajax({
                url: '/dashboard/inbox-rejectservice/',
                type: "POST",
                cache: false,
                processData: false,
                contentType: false,
                async: false,
                data : formData,
                enctype: "multipart/form-data",
                success: function(json) {
                    $("#reject-modal" + oi_pk).modal("hide");
                    $('#reject_success_modal').modal("show");
                    $('#reject-form-id' + oi_pk)[0].reset();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                    window.location.reload();
                }
            });

        }
        
    });
   
};

function acceptService(oi_pk) {
    if (oi_pk){
        $("#accept-modal" + oi_pk).modal("show");
        $(document).on('click', '#accept-submit-button' + oi_pk, function () {
            var formData = $('#accept-form-id' + oi_pk).serialize();
            $.ajax({
                url: '/dashboard/inbox-acceptservice/',
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(data) {
                    $("#accept-modal" + oi_pk).modal("hide");
                    $("#reject-message-id").text('Thank you for accepting draft.');
                    $('#reject_success_modal').modal("show");
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong, try after sometimes");
                }
            });
        });
 
    }
};

function downloadOrderInvoice(order_pk) {
    if (order_pk){
        $('#download-invoice-form' + order_pk).submit();
    }
};


function downloadOrderTemplate(order_pk) {
    if(order_pk){
        $('#download-resume-form' + order_pk).submit();
    }
}

function openCancelModal(order_pk) {
    modal_id = "#cancelorder_div" + order_pk
    $(modal_id).modal('show');
}





$(document).ready(function(){

    // $(document).on('click', '#download-order-invoice', function () {
    //     $('#').submit();
    // });

    $(document).on('click', '#load-more-orderitem', function(event) {
        this.disabled = true;
        var formData = $("#load-orderitem-form").serialize();
        $.ajax({
            url : "/dashboard/loadmore/orderitem/",
            type: "POST",
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                // data = JSON.parse(data);
                $("#load_more_item").remove();
                $("#orderitem-inbox-box").append(data.orderitem_list);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more comments.");
            }
        });   
    });

    $(document).on('change', '#lastmonth-id', function(event) {

        var formData = $("#order-filter-form").serialize();
        $.ajax({
            url : "/dashboard/inbox-filter/",
            type: "POST",
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                $("#orderitem-inbox-box").html(data.orderitem_list);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("something went wrong, try again later");
            }
        });   
    });

    $(document).on('change', '#select-type-id', function(event) {
        var formData = $("#order-filter-form").serialize();
        $.ajax({
            url : "/dashboard/inbox-filter/",
            type: "POST",
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                $("#orderitem-inbox-box").html(data.orderitem_list);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("something went wrong, try again later");
            }
        }); 
    });


    $("#reject_success_modal").on('hidden.bs.modal', function () {
        window.location.reload();
    });

    $.validator.addMethod("extnAccept", function(value, element) {
        var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
        if(value && !allowedExtensions.exec(value)){
            return false;
        }
        else{
            return true;
        }
            
    });

    $.validator.addMethod("extn", function(value, element) {
        var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
        if(value && !allowedExtensions.exec(value)){
            return false;
        }
        else{
            return true;
        }
            
    });

    $(document).on('click', '#upload-resume-button', function () {
        $("#resume-upload-form").validate({
            rules:{
                file:{
                    required: function(element) {
                        if ($("#shine-res").is(":checked"))
                            return false;
                        else
                            return true;
                    },
                    maxlength: 200,
                    extnAccept: true,
                },
            },
            messages:{
                file:{
                    required: 'this value is required.',
                    maxlength: 'length should be less than 200 characters',
                    extnAccept: 'only pdf, doc and docx formats are allowed',
                },
                shine_resume:{
                    required: 'this value is required.',
                }
            },

            highlight: function(element) {
                $(element).closest('.file-box').addClass('error')
            },
            unhighlight: function(element) {
                $(element).closest('.file-box').removeClass('error')
            },
            errorPlacement: function(error, element){
                $(element).closest('.file-box').find(".error-txt").html(error.text());
            }

        });

        var flag = $("#resume-upload-form").valid();
        var required_flag = false

        $('input[name="resume_pending"]').each(function () {
            if ($(this).is(':checked')){
                required_flag = true;
            }
        });

        if (!required_flag){
            $('#required_product_error').text('select atleast one of services');
        }

        if (flag && required_flag){
            $('#resume-upload-form').submit();
        }
    });

    $(document).on('click', '[name="resume_pending"]', function () {
        $('#required_product_error').text('');
    });

    $(document).on('click', '#shine-res', function () {
        if ($(this).is(':checked')){
            $('#file-error').text('');
        }
        else{
            $('#file-error').text('this value is required');
        }
    });

    $(document).on('click', '.upload-resume', function () {
        $.ajax({
            url: '/dashboard/inbox-notificationbox/',
            type: 'GET',
            dataType: 'html',
            success: function(html) {
                $('#notification-box-id').html(html);
                window.scrollTo(0, 0);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        }); 
    });

    $.validator.addMethod("custom_message",
        function(value, element) {
            if($('#id_comment').val().trim()){
                return true;
            }
            return false;
    });

     $.validator.addMethod("custom_review",
         function(value, element) {
             if($('#id_review').val().trim()){
                 return true;
             }
             return false;
     });

    $(document).on('click', '[name="rating"]', function () {
        var flavour = $('[name="flavour"]').val();
        console.log(flavour);
        if (flavour == 'mobile'){
            var rating_val = $(this).attr('value');
            $('#selected-rating').text(rating_val);
        }
        else {
            var html = $(this).attr('value') + '<small>/5</small>';
            $('#selected-rating').html(html);
        }
        $('#rating-error').text('');
       
    });

    $(document).on('click', '#rating-submit', function () {
        $("#feedback-form").validate({
            rules: {
                rating:{
                    required: true,
                },
                review: {
                    maxlength: 1500,
                    custom_review:true,
                },
            },
            messages: {
                rating:{
                    required: "rating is required."
                },
                review: {
                    maxlength: "length should not be greater than 1500 characters.",
                },
            },
            errorPlacement: function(error, element){
                $(element).siblings('.error').html(error.text());
            },
            submitHandler: function(form) {                
                return false;
            },

        });
        var flag = $('#feedback-form').valid();
        var rating_flag = false;
        $('input[name="rating"]').each(function () {
            if ($(this).is(':checked')){
                rating_flag = true;
            }
        });
        if (!rating_flag){
            $('#rating-error').text('rating is mandatory');
        }
        if (flag && rating_flag){
            var formData = $('#feedback-form').serialize();
            $(this).attr('disabled','true')
            $.ajax({
                url: '/dashboard/inbox-feedback/',
                type: 'POST',
                data : formData,
                dataType: 'json',
                success: function(json) {
                    alert(json.display_message);
                    window.location = window.location.href.split('?')[0];
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong, try again later");
                }
            });
        }
        
        
    });

    $(document).on('click', '#comment_submit_button', function () {
        $("#user-comment-form").validate({
            rules: {
                comment: {
                    required: true,
                    maxlength: 200,
                    custom_message: true,
                },
            },
            messages: {
                comment: {
                    required: "Message is Mandatory.",
                    maxlength: "Length should be less than 200 characters.",
                    custom_message: "Message is Mandatory.",
                },
            },
            errorPlacement: function(error, element){
                $(element).siblings('.error').html(error.text());
            },

        });
        var flag = $('#user-comment-form').valid();

        if (flag){
            var flavour = $('[name="flavour"]').val();
            if (flavour == "mobile"){
                $('#user-comment-form').submit();
                $('#user-comment-form').reset();
            }
            else{
                var formData = $('#user-comment-form').serialize();
                $.ajax({
                    url: '/dashboard/inbox-comment/',
                    type: 'POST',
                    data : formData,
                    dataType: 'html',
                    success: function(html) {
                        $('#right-content-id').html(html);
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                        alert("Something went wrong");
                    }
                });
            }
        }
    });

});


function updateTabContent(ajaxurl, element1, element2){
    $.ajax({
        url: ajaxurl,
        type: "get",
        success: function(response){
            result = JSON.parse(response);
            if(!result.response){
                alert("Sorry! Something went wrong. You can also use your services on " +
                    "http://www.roundone.in/ or you can reach out at support@roundone.in.", "Ok");
            }
            $(element2).html(result.template);
        },
        failure: function(response){
            alert("Sorry! Something went wrong. You can also use your services on " +
                "http://www.roundone.in/ or you can reach out at support@roundone.in.", "Ok", "Cancel");
        },
    });
}

$("#tab_upcoming").on("click", function(e){
    ajaxurl = "/dashboard/roundone/upcoming/";
    element1 = "#tab_upcoming";
    element2 = "#upcoming";
    updateTabContent(ajaxurl, element1, element2);
});

$("#tab_past_interaction").on("click", function(e){
    ajaxurl = "/dashboard/roundone/past/";
    element1 = "#tab_past_interaction";
    element2 = "#past";
    updateTabContent(ajaxurl, element1, element2);
});

$("#tab_saved").on("click", function(e){
    ajaxurl = "/dashboard/roundone/saved/";
    element1 = "#tab_saved";
    element2 = "#Saved";
    updateTabContent(ajaxurl, element1, element2);
});

function onClickDeleteJob(idx){
    $.ajax({
        url: "/dashboard/roundone/saved/delete/",
        type: "post",
        data: $("#id_"+idx).serialize(),
        success: function(response){
            result = JSON.parse(response);
            if(result.status){
                window.location.reload();
            }else{
                showSuccessModal(result.message, "Ok", "Cancel");
            }
        },
        failure: function(response){
            showErrorModal("Error deleting this job", "Ok", "Cacnel");
        },
        complete: function(response){
            if(element.length > 0){
                $(element).addClass("active");
            }
        }
    });
}

    // Personal
    $("#edit_roundone_personal").on("click", function(){
        $("#form_roundone_personal").show();
        $("#detail_roundone_personal").hide();
    });
    
    $(".js_edit_education_btn").on("click", function(){
        $("#form_edit_education").show();
        $("#div_education").hide();
    });

    $("#cancel_roundone_personal").on("click", function(){
        // $("#form_roundone_personal").hide();
        $("#detail_roundone_personal").show();     
    });

    $("#form_roundone_personal").validate({
        errorClass: "roundone-error",
        rules:{
            name: {
                required: true,
                minlength: 2,
                maxlength: 60
            },
            mobile: {
                required: true,
                number: true,
                maxlength: 10
            },
            gender: {
                required: true
            },
            // total_exp: {
            //     required: true,
            //     number: true
            // }
        },
        messages: {
            name: {
                required: "Please enter  your name",
                minlength: "At least 2 character",
                maxlength: "At most 30 characters"
            },
            contact: {
                required: "Please enter contact number",
                number: "Only digits",
                maxlength: "At most 10 digits"
            },
            gender: {
                required: "This is required"
            },
            total_exp: {
                required: "Please enter your experience",
                number: "Only digits"
            }
        },
        submitHandler: function(form){
            ajaxurl = $("input[name=post_personal_detail]").val();
            roundone_edit(form, ajaxurl);
        },
        highlight:function(el){
            switch(el.type)
            {   
                default:
                    $(el).addClass('redborder');
                    break;
            }
        },
        unhighlight:function(el){
            switch(el.type)
            {
                default:
                    $(el).removeClass('redborder');
                    break;
            }
        },

    });

    // Add Education
    $("#add_roundone_education").on("click", function(){
        $("#form_add_education").show();
    });

    $("#cancel_add_education").on("click", function(){
        $("#form_add_education").hide();
    });

    function validateYear(year_value){
        if($("#today_date").val()){
            var today = new Date($("#today_date").val());
        }else{
            var today = new Date();
        }
        upper_year = today.getFullYear() + 5;
        if(year_value > upper_year){
            showErrorModal("Passing Year cant be greater than " + upper_year.toString(), "Ok");
            return false;
        }
        return true;
    }

    $("#form_edit_education").validate({
        errorClass: "roundone-error",
        // rules:{
        //     institute: {
        //         required: true,
        //         minlength: 2,
        //         maxlength: 40
        //     },
        //     degree: {
        //         required: true,
        //         minlength: 2,
        //         maxlength: 40
        //     },
        //     major: {
        //         required: true,
        //         minlength: 2,
        //         maxlength: 40
        //     },
        //     year: {
        //         required: true,
        //         number: true,
        //         minlength: 4,
        //         maxlength: 4
        //     },
        //     marks:{
        //         required: true,
        //         validmarks: true
        //     }
        // },
        // messages: {
        //     institute: {
        //         required: "Please enter  institute name",
        //         minlength: "At least 2 character",
        //         maxlength: "At most 40 character"
        //     },
        //     degree: {
        //         required: "Please enter degree name",
        //         minlength: "At least 2 character",
        //         maxlength: "At most 40 character"
        //     },
        //     major: {
        //         required: "This is required",
        //         minlength: "At least 2 character",
        //         maxlength: "At most 40 character"
        //     },
        //     year: {
        //         required: "Please enter year of passing",
        //         number: "Only digits",
        //         minlength: "At least 4 digits",
        //         maxlength: "At most 4 digits"
        //     }
        // },
        submitHandler: function(form){
            ajaxurl = $("input[name=post_education]").val();
            roundone_edit(form, ajaxurl);
        },
        highlight:function(el){
            switch(el.type)
            {   
                default:
                    $(el).addClass('redborder');
                    break;
            }
        },
        unhighlight:function(el){
            switch(el.type)
            {
                default:
                    $(el).removeClass('redborder');
                    break;
            }
        },

    });

    // Edit Education
    // $("#edit_work_ex").on("click", function(){
    //     $("#form_edit_education").show();
    //     $("#div_education").hide();
    // });
    
    // Edit Workex
    $("#js_edit_workex").on("click", function(){
        $("#form_edit_workex").show();
        $('#div_workex').hide();
    });

    // // Add Workexp
    // $("#add_roundone_workex").on("click", function(){
    //     $("#form_add_workex").show();
    // });

    // $("#cancel_add_workex").on("click", function(){
    //     $("#form_add_workex").hide();
    // });


    $("#form_edit_workex").validate({
        errorClass: "roundone-error",
        rules:{
            company: {
                required: true,
                minlength: 2
            },
            position: {
                required: true,
                minlength: 2
            },
            from: {
                required: true,
                // date: true
            },
            to:{
                required: true
                // date:true
            }
        },
        messages: {
            company: {
                required: "Please mention company name",
                minlength: "At least 2 characters"
            },
            position: {
                required: "Please mention Job Title",
                minlength: "At least 2 characters"
            },
            from: {
                required: "From Date is mandatory",
                date: "Must be a valid date"
            },
            to:{
                date: "Must be a valid date"
            }
        },
        submitHandler: function(form){
            ajaxurl = $("input[name=post_workex_detail]").val();
            roundone_edit(form, ajaxurl);
        },
        highlight:function(el){
            switch(el.type)
            {   
                default:
                    $(el).addClass('redborder');
                    break;
            }
        },
        unhighlight:function(el){
            switch(el.type)
            {
                default:
                    $(el).removeClass('redborder');
                    break;
            }
        },

    });

    // Upload Resume
    $("#resume_form").validate({
        errorClass: "roundone-error",
        rules:{
            resume:{
                required: true,
                // extension: "doc|docx|pdf"
            }
        },
        messages:{
            resume:{
                required: "Resume is required",
                // extension: "Please select doc, docx or pdf"
            }
        },
        submitHandler: function(form){
            posturl = $(form).data().url;
            var formData = new FormData(form);
            $.ajax({
                url: posturl,
                method: "POST",
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                failure: function(response){
                    alert("Error while updating resume, Please retry");
                },
                complete: function(result){
                    var rsp =  $.parseJSON(result.responseText);
                    if(rsp.status)
                    {
                        alert("Resume Updated successfully");
                        $('#upload-file-info').html('');
                        $("#error_id").html(rsp.msg.non_field_errors).hide();
                        window.location.reload();
                    }
                    else if(rsp.status == false)
                    {
                        $("#error_id").html(rsp.msg.non_field_errors).show();
                    }
                    else
                    {
                        alert('Resume is not updated')
                    }
                }
            });
        },
        // highlight:function(el, error){
        //     switch(el.type)
        //     {   
        //         default:
        //             error.appendTo(".error-txt");
        //             break;
        //     }
        // },
        // unhighlight:function(el){
        //     switch(el.type)
        //     {
        //         default:
        //             $(el).removeClass('redborder');
        //             break;
        //     }
        // },
        errorPlacement: function(error, element) {
            if (element.attr("name") == "resume")
            {
                error.appendTo(".error-txt");
            }           
        }
    });


function roundone_edit(form, ajaxurl){
    $.ajax({
        url: ajaxurl,
        method: "post",
        data: $(form).serialize(),
        success: function(response){
            response_json = JSON.parse(response);
            if(response_json.status){
                alert("Successfully Updated");
                window.location.reload();                
            }
            else
            {
                alert(response_json.msg);
                window.location.reload();
            }
        },
        complete: function(response){
            hideLoader();
        },
        failure: function(response){
            alert("Error while editing, Please retry");
        }
    });
}

const uploadResumeShine = (checkbox,order_id)=>{
    let request = fetch(`/order/api/v1/${order_id}/update/`,{
        headers: {
            "Content-Type": "application/json"
        },
        method: 'PATCH',  
        body: JSON.stringify({
                    service_resume_upload_shine: $(checkbox).is(':checked')
                }),
    });

    request.then((resp) =>resp.json())
    .then(response => {
        console.log('--response', response);
        title = response['service_resume_upload_shine'] ? 'Resume will be updated' : 'Resume will not be updated'
        Toast.fire({
                    type: response['service_resume_upload_shine'] ?'success' : 'error',
                    title
        })
    })
    .catch(e =>{
        Toast.fire({
            type: 'error',
            title:'Something went wrong'
        })
    })
}
