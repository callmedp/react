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

// function onClickEditMyProfile(){
//     $.ajax({
//         url: "/dashboard/myprofile/edit/",
//         type: "get",
//         data: $("#id_"+idx).serialize(),
//         success: function(response){
//             hideLoader();
//             result = JSON.parse(response);
//             if(result.status){
//                 window.location.reload();
//             }else{
//                 showSuccessModal(result.message, "Ok", "Cancel");
//             }
//         },
//         failure: function(response){
//             showErrorModal("Error editing the profile", "Ok", "Cacnel");
//         },
//         complete: function(response){
//             if(element.length > 0){
//                 $(element).addClass("active");
//             }
//             hideLoader();
//         }
//     });
// }

// $("#id_feedback").validate({
//     errorClass: "feedback-error",
//     rules:{
//         roundoneRating: {
//             required: true
//         },
//         inlineRadioOptions: {
//             required: true
//         }
//     },
//     messages: {
//         roundoneRating: {
//             required: "Please provide rating."
//         },
//         inlineRadioOptions: {
//             required: "Please choose at least one."
//         }
//     },
//     submitHandler: function(form){
//         feedback_submit(form);
//     },
//     highlight:function(el){
//         switch(el.type)
//         {
//             default:
//                 $(el).addClass('redborder');
//                 break;
//         }
//     },
//     unhighlight:function(el){
//         switch(el.type)
//         {
//             default:
//                 $(el).removeClass('redborder');
//                 break;
//         }
//     },

// });

// function postLoadContent(){
//     $("#id_confirm_interaction").on("click", function(e){
//         showLoader();
//         var dom_data = $(this).data();
//         requestId = dom_data.request;
//         ajaxurl = $("input[name=dashboard_referral_confirm]").val();
//         $.ajax({
//             url: ajaxurl,
//             type: "get",
//             data: {'requestId': requestId},
//             success: function(response){
//                 hideLoader();
//                 result = JSON.parse(response);
//                 if(result.status){
//                     window.location.reload();
//                 }else{
//                     showSuccessModal(result.message, "Ok", "Cancel");
//                 }
//             },
//             failure: function(response){
//                 showErrorModal("Error confirming this interaction, Please Retry", "Ok", "Cacnel");
//             },
//             complete: function(response){
//                 hideLoader();
//             }
//         });
//     });

    // Personal
    $("#edit_roundone_personal").on("click", function(){
        $("#form_roundone_personal").show();
        $("#detail_roundone_personal").hide();
    });

    $("#cancel_roundone_personal").on("click", function(){
        $("#form_roundone_personal").hide();
        $("#detail_roundone_personal").show();
    });

    $("#form_roundone_personal").validate({
        errorClass: "roundone-error",
        rules:{
            name: {
                required: true,
                minlength: 2,
                maxlength: 30
            },
            mobile: {
                required: true,
                number: true,
                maxlength: 10
            },
            // gender: {
            //     required: true
            // },
            total_exp: {
                required: true,
                number: true
            }
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
            // gender: {
            //     required: "This is required"
            // },
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

    $("#form_add_education").validate({
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
            var year_value = 0;
            var formData = $(form).serializeArray();
            for(idx in formData){
                if(formData[idx].name.indexOf("year") == 0){
                    year_value = parseInt(formData[idx].value);
                }
            }
            if(validateYear(year_value)){
                ajaxurl = $("input[name=roundone_add_education]").val();
                roundone_edit(form, ajaxurl);
            }
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
        idx = $(this).data().idx;
        edu_div = "#div_education" + idx.toString();
        form = "#form_edit_education" + idx.toString();
        $(edu_div).hide();
        $(form).show();
    });

    // $(".js_cancel_edit_education").on("click", function(){
    //     idx = $(this).data().idx;
    //     edu_div = "#div_education" + idx.toString();
    //     form = "#form_edit_education" + idx.toString();
    //     $(edu_div).show();
    //     $(form).hide();
    // });

    $(".js_form_edit_education").each(function(index, item){
        $(item).validate({
            errorClass: "roundone-error",
            submitHandler: function(form){
                var year_value = 0;
                var formData = $(form).serializeArray();
                for(idx in formData){
                    if(formData[idx].name.indexOf("year") == 0){
                        year_value = parseInt(formData[idx].value);
                    }
                }
                if(validateYear(year_value)){
                    ajaxurl = $(form).data().url;
                    roundone_edit(form, ajaxurl);
                }
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
    });


    $(".js_institute").each(function(index, item){
        $(item).rules("add", {
            required: true,
            minlength: 2,
            maxlength: 40,
            messages:{
                required: "Please enter  institute name",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            }
        });
    });

    $(".js_degree").each(function(index, item){
        $(item).rules("add", {
            required: true,
            minlength: 2,
            maxlength: 40,
            messages:{
                required: "Please enter  institute name",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            }
        });
    });

    $(".js_major").each(function(index, item){
        $(item).rules("add", {
            required: true,
            minlength: 2,
            maxlength: 40,
            messages:{
                required: "Please enter  institute name",
                minlength: "At least 2 character",
                maxlength: "At most 40 character"
            }
        });
    });

    $(".js_year").each(function(index, item){
        $(item).rules("add", {
            required: true,
            number: true,
            minlength: 4,
            maxlength: 4,
            messages: {
                required: "Please enter year of passing",
                number: "Only digits",
                minlength: "At least 4 digits",
                maxlength: "At most 4 digits"
            }
        });
    });

    $(".js_marks").each(function(index, item){
        $(item).rules("add", {
            required: true,
            validmarks: true,
            maxlength: 6,
            messages: {
                required: "Please enter your marks.",
                maxlength: ""
            }
        });
    });

    
//     // Add Workexp
//     $("#add_roundone_workex").on("click", function(){
//         $("#form_add_workex").show();
//     });

//     $("#cancel_add_workex").on("click", function(){
//         $("#form_add_workex").hide();
//     });

//     function validateDate(fdate, tdate, is_current){
//         if($("#today_date").val()){
//             var today = new Date($("#today_date").val());
//         }else{
//             var today = new Date();
//         }
//         var from_date = new Date(fdate);
//         if(from_date > today){
//             showErrorModal("From Date cant be greater than today", "Ok");
//             return false;
//         }
//         if(!is_current){
//             if(tdate){
//                 var to_date = new Date(tdate);
//                 if(to_date > today){
//                     showErrorModal("To Date cant be greater than today", "Ok");
//                     return false;
//                 }
//                 if(from_date > to_date){
//                     // from_date cant be greater than to_date
//                     showErrorModal("From Date cant be greater than To Date", "Ok");
//                     return false;
//                 }
//             }else{
//                 // to_date is mandatory
//                 showErrorModal("Please provide valid to date", "Ok");
//                 return false;
//             }
//         }
//         return true;
//     }

//     $("#form_add_workex").validate({
//         errorClass: "roundone-error",
//         rules:{
//             company: {
//                 required: true,
//                 minlength: 2
//             },
//             position: {
//                 required: true,
//                 minlength: 2
//             },
//             from: {
//                 required: true,
//                 date: true
//             },
//             to:{
//                 date:true
//             }
//         },
//         messages: {
//             company: {
//                 required: "Please mention company name",
//                 minlength: "At least 2 characters"
//             },
//             position: {
//                 required: "Please mention Job Title",
//                 minlength: "At least 2 characters"
//             },
//             from: {
//                 required: "From Date is mandatory",
//                 date: "Must be a valid date"
//             },
//             to:{
//                 date: "Must be a valid date"
//             }
//         },
//         submitHandler: function(form){
//             from_date = false;
//             to_date = false;
//             current = false;
//             var formData = $(form).serializeArray();
//             for(idx in formData){
//                 if(formData[idx].name.indexOf("from") == 0){
//                     from_date = formData[idx].value;
//                 }
//                 if(formData[idx].name.indexOf("to") == 0){
//                     to_date = formData[idx].value;
//                 }
//                 if(formData[idx].name.indexOf("current") == 0){
//                     current = true;
//                 }
//             }
//             if(validateDate(from_date, to_date, current)){
//                 ajaxurl = $("input[name=roundone_add_workex]").val();
//                 roundone_edit(form, ajaxurl);
//             }
//         },
//         highlight:function(el){
//             switch(el.type)
//             {   
//                 default:
//                     $(el).addClass('redborder');
//                     break;
//             }
//         },
//         unhighlight:function(el){
//             switch(el.type)
//             {
//                 default:
//                     $(el).removeClass('redborder');
//                     break;
//             }
//         },

//     });

//     // Edit Workex
//     $(".js_edit_workex_btn").on("click", function(){
//         idx = $(this).data().idx;
//         edu_div = "#div_workex" + idx.toString();
//         form = "#form_edit_workex" + idx.toString();
//         $(edu_div).hide();
//         $(form).show();
//     });

//     $(".js_cancel_edit_workex").on("click", function(){
//         idx = $(this).data().idx;
//         edu_div = "#div_workex" + idx.toString();
//         form = "#form_edit_workex" + idx.toString();
//         $(edu_div).show();
//         $(form).hide();
//     });

//     $(".js_form_edit_workex").each(function(index, item){
//         $(item).validate({
//             errorClass: "roundone-error",
//             submitHandler: function(form){
//                 from_date = false;
//                 to_date = false;
//                 current = false;
//                 var formData = $(form).serializeArray();
//                 for(idx in formData){
//                     if(formData[idx].name.indexOf("from") == 0){
//                         from_date = formData[idx].value;
//                     }
//                     if(formData[idx].name.indexOf("to") == 0){
//                         to_date = formData[idx].value;
//                     }
//                     if(formData[idx].name.indexOf("current") == 0){
//                         current = true;
//                     }
//                 }
//                 if(validateDate(from_date, to_date, current)){
//                     ajaxurl = $(form).data().url;
//                     roundone_edit(form, ajaxurl);
//                 }
//             },
//             highlight:function(el){
//                 switch(el.type)
//                 {   
//                     default:
//                         $(el).addClass('redborder');
//                         break;
//                 }
//             },
//             unhighlight:function(el){
//                 switch(el.type)
//                 {
//                     default:
//                         $(el).removeClass('redborder');
//                         break;
//                 }
//             },

//         });
//     });

//     $(".js_company").each(function(index, item){
//         $(item).rules("add", {
//             required: true,
//             minlength: 2,
//             messages:{
//                 required: "Please enter company name",
//                 minlength: "At least 2 character"
//             }
//         });
//     });

//     $(".js_position").each(function(index, item){
//         $(item).rules("add", {
//             required: true,
//             minlength: 2,
//             messages:{
//                 required: "Please enter job title",
//                 minlength: "At least 2 character"
//             }
//         });
//     });

//     $(".js_from").each(function(index, item){
//         $(item).rules("add", {
//             required: true,
//             date: true,
//             messages:{
//                 required: "Please enter valid date",
//                 date: "Must be a valid date"
//             }
//         });
//     });

//     $(".js_to").each(function(index, item){
//         $(item).rules("add", {
//             date: true,
//             messages:{
//                 date: "Must be a valid date"
//             }
//         });
//     });

//     // Add Skill
//     $("#add_roundone_skill").on("click", function(){
//         $("#form_add_skill").show();
//     });

//     $("#cancel_add_skill").on("click", function(){
//         $("#form_add_skill").hide();
//     });

//     $("#form_add_skill").validate({
//         errorClass: "roundone-error",
//         rules:{
//             skill: {
//                 required: true,
//                 minlength: 2
//             }
//         },
//         messages: {
//             skill: {
//                 required: "Please mention at least one skill",
//                 minlength: "At least 2 characters"
//             }
//         },
//         submitHandler: function(form){
//             ajaxurl = $("input[name=roundone_add_skill]").val();
//             roundone_edit(form, ajaxurl);
//         },
//         highlight:function(el){
//             switch(el.type)
//             {   
//                 default:
//                     $(el).addClass('redborder');
//                     break;
//             }
//         },
//         unhighlight:function(el){
//             switch(el.type)
//             {
//                 default:
//                     $(el).removeClass('redborder');
//                     break;
//             }
//         },

//     });

//     // Edit Skill
//     $(".js_edit_skill").on("click", function(){
//         $("#div_all_skill").hide();
//         $("#form_edit_skill").show();
//     });

//     $("#cancel_edit_skill").on("click", function(){
//         $("#div_all_skill").show();
//         $("#form_edit_skill").hide();
//     });

//     $("#form_edit_skill").validate({
//         errorClass: "roundone-error",
//         rules:{
//             skill: {
//                 required: true,
//                 minlength: 2
//             }
//         },
//         messages: {
//             skill: {
//                 required: "Please mention at least one skill",
//                 minlength: "At least 2 characters"
//             }
//         },
//         submitHandler: function(form){
//             ajaxurl = $(form).data().url;
//             roundone_edit(form, ajaxurl);
//         },
//         highlight:function(el){
//             switch(el.type)
//             {   
//                 default:
//                     $(el).addClass('redborder');
//                     break;
//             }
//         },
//         unhighlight:function(el){
//             switch(el.type)
//             {
//                 default:
//                     $(el).removeClass('redborder');
//                     break;
//             }
//         },

//     });

//     // Start Applying
//     $("#start_apply").on("click", function(){
//         idx = $(this).data().idx;
//         if (idx){
//             GetReference(idx);
//         }else{
//             window.location.href = $("input[name=partner-home]").val();
//         }
//     });
    
//     // Upload Resume
//     $("#resume_form").validate({
//         errorClass: "roundone-error",
//         rules:{
//             resume:{
//                 required: true,
//                 extension: "doc|docx|pdf"
//             }
//         },
//         messages:{
//             resume:{
//                 required: "Resume is required",
//                 extension: "Please select doc, docx or pdf"
//             }
//         },
//         submitHandler: function(form){
//             showLoader();
//             posturl = $(form).data().url;
//             var formData = new FormData(form);
//             $.ajax({
//                 url: posturl,
//                 method: "POST",
//                 data: formData,
//                 cache: false,
//                 contentType: false,
//                 processData: false,
//                 failure: function(response){
//                     showErrorModal("Error while updating resume, Please retry", "Ok");
//                 },
//                 complete: function(response){
//                     showSuccessModal("Resume Updated successfully", "Ok");
//                     ajaxurl = "/dashboard/roundone/profile/?profile_reload=1";
//                     element = "#tab_roundone_profile";
//                     updateTabContent(ajaxurl, element);
//                 }
//             });
//         },
//         highlight:function(el){
//             switch(el.type)
//             {   
//                 default:
//                     $(el).addClass('redborder');
//                     break;
//             }
//         },
//         unhighlight:function(el){
//             switch(el.type)
//             {
//                 default:
//                     $(el).removeClass('redborder');
//                     break;
//             }
//         },
//     })
// }

// function feedback_submit(form){
//     showLoader();
//     ajaxurl = $("input[name=form_feedback]").data().url;
//     $.ajax({
//         url: ajaxurl,
//         method: "post",
//         data: $(form).serialize(),
//         success: function(response){
//             response_json = JSON.parse(response);
//             if(response_json.status){
//                 $("#feedback").html('');
//                 $("#id_interaction_result").html(response_json.template)
//             }else{
//                 showSuccessModal(response_json.message, "Ok", "Cancel");
//             }
//         },
//         failure: function(response){
//             showErrorModal("Error Submitting feedback", "Ok", "Cancel");
//         },
//         complete: function(response){
//             hideLoader();
//         }
//     });
// }

function roundone_edit(form, ajaxurl){
    showLoader();
    $.ajax({
        url: ajaxurl,
        method: "post",
        data: $(form).serialize(),
        success: function(response){
            response_json = JSON.parse(response);
            if(response_json.status){
                alert(response_json.message)
                // window.location.reload()
                // showSuccessModal(response_json.message, "Ok");
                // loadurl = "/dashboard/roundone/profile/?profile_reload=1";
                // element = "#tab_roundone_profile";
                // updateTabContent(loadurl, element);
            }
            // else
            // {
            //     showErrorModal(response_json.message, "Ok");
            // }
        },
        complete: function(response){
            hideLoader();
        },
        failure: function(response){
            showErrorModal("Error while editing, Please retry", "Ok");
        }
    });
}
