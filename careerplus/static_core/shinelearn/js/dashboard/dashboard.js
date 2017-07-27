function viewDetailOrderitem(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/detail/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
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
            url: '/user/dashboard/comment/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        });
    }
};

function rejectService(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/rejectservice/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'json',
            success: function(data) {
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
            }
        });
    }
};

function acceptService(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/acceptservice/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'json',
            success: function(data) {
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
            }
        });
    }
};



$(document).ready(function(){

    $.validator.addMethod("extnAccept", function(value, element) {
        var fileInput = document.getElementById('file-id');
        var filePath = fileInput.value;
        console.log(filePath);
        var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
        if(!allowedExtensions.exec(filePath)){
            return false;
        }
        else{
            return true;
        }
            
    });

    $("#resume-upload-form").validate({
        rules: {
            file:{
                required: true,
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
        },
        // highlight: function(element) {
        //     $(element).closest('.input-file').addClass('error');
        // },
        // unhighlight: function(element) {
        //     $(element).closest('.input-file').removeClass('error');
        // },
        // errorPlacement: function(error, element){
        //     $(element).closest('.error-txt').html(error.text());
        // }
    });

    $('#upload-resume-button').click(function(){
        var flag = $("#resume-upload-form").valid();
        if (flag){
            $('#resume-upload-form').submit();
        }
    });

    $.validator.addMethod("custom_message",
        function(value, element) {
            if($('#id_comment').val().trim()){
                return true;
            }
            return false;
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
        console.log(flag);
        if (flag){
            var formData = $('#user-comment-form').serialize();
            $.ajax({
                url: '/user/dashboard/comment/',
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
    });

});


function updateTabContent(ajaxurl, element1, element2){
    $.ajax({
        url: ajaxurl,
        type: "get",
        success: function(response){
            result = JSON.parse(response);
            if(!result.response){
                alert("Roundone is facing technical issue. Please try again.", "Ok");
            }
            $(element2).html(result.template);
        },
        failure: function(response){
            alert("Roundone is facing technical issue. Error getting profile. Please try again.", "Ok", "Cancel");
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
        rules:{
            institute: {
                required: true,
                minlength: 2,
                maxlength: 40
            },
            degree: {
                required: true,
                minlength: 2,
                maxlength: 40
            },
            major: {
                required: true,
                minlength: 2,
                maxlength: 40
            },
            year: {
                required: true,
                number: true,
                minlength: 4,
                maxlength: 4
            },
            marks:{
                required: true,
                validmarks: true
            }
        },
        messages: {
            institute: {
                required: "Please enter  institute name",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            },
            degree: {
                required: "Please enter degree name",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            },
            major: {
                required: "This is required",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            },
            year: {
                required: "Please enter year of passing",
                number: "Only digits",
                minlength: "At least 4 digits",
                maxlength: "At most 4 digits"
            }
        },
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
    $(".js_edit_education_btn").on("click", function(){
        $("#div_education").hide();
        $("#form_edit_education").show();
    });

    // Add Workexp
    $("#add_roundone_workex").on("click", function(){
        $("#form_add_workex").show();
    });

    $("#cancel_add_workex").on("click", function(){
        $("#form_add_workex").hide();
    });


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

    // Edit Workex
    $(".js_edit_workex_btn").on("click", function(){
        $('#div_workex').hide();
        $("#form_edit_workex").show();
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
                complete: function(response){
                    if(response.status)
                    {
                        alert("Resume Updated successfully");
                    }
                    else
                    {
                        alert("Resume not Updated");
                    }
                }
            });
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
    })


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
