$('document').ready(function(){
});

function showSuccessModal(message, accept, reject, accept_nav, reject_nav, onclose){
    $("#id_success_accept").unbind("click");
    $("#id_success_reject").unbind("click");
    $("#api_rsp").modal('show');
    $("#id_success_message").html(message);
    if(accept && accept.length > 0){
        $("#id_success_accept").html(accept);
    }else{
        $("#id_success_accept").hide();
    }

    if(reject && reject.length > 0){
        $("#id_success_reject").html(reject);
    }else{
        $("#id_success_reject").hide();
    }

    // clicking accept
    $("#id_success_accept").on("click", function(){
        $("#api_rsp").hide();
        if(accept_nav && accept_nav.length > 0){
            this_url = window.location.href;
            if(this_url == accept_nav){
                window.location.reload();
            }else{
                window.location.href = this_url;
            }
        }
        window.location.reload();
    });

    // clicking accept
    $("#id_success_reject").on("click", function(){
        $("#id_success_modal").hide();
        if(reject_nav && reject_nav.length > 0){
            this_url = window.location.href;
            if(this_url == reject_nav){
                window.location.reload();
            }else{
                window.location.href = reject_nav;
            }
        }
    });

    $("#id_close_success_modal").on("click", function(){
        if(onclose && onclose.length > 0){
            this_url = window.location.href;
            if(this_url == onclose){
                window.location.reload();
            }else{
                window.location.href = onclose;
            }
        }
    });

}

function showErrorModal(message, accept, reject, accept_nav, reject_nav, onclose){
    $("#id_error_accept").unbind("click");
    $("#id_error_reject").unbind("click");
    $("#api_rsp_error").modal('show');
    $("#id_error_message").html(message);
    if(accept && accept.length > 0){
        $("#id_error_accept").html(accept);
    }else{
        $("#id_error_accept").hide();
    }

    if(reject && reject.length > 0){
        $("#id_error_reject").html(reject);
    }else{
        $("#id_error_reject").hide();
    }

    // clicking accept
    $("#id_error_accept").on("click", function(){
        $("#api_rsp_error").hide();
        if(accept_nav && accept_nav.length > 0){
            this_url = window.location.href;
            if(this_url == accept_nav){
                window.location.reload();
            }else{
                window.location.href = accept_nav;
            }
        }
        else
        {
          window.location.reload();  
        }
    });

    // clicking accept
    $("#id_error_reject").on("click", function(){
        $("#id_error_modal").modal('hide');
        if(reject_nav && reject_nav.length > 0){
            this_url = window.location.href;
            if(this_url == reject_nav){
                window.location.reload();
            }else{
                window.location.href = reject_nav;
            }
        }
    });

    $("#id_close_error_modal").on("click", function(){
        if(onclose && onclose.length > 0){
            this_url = window.location.href;
            if(this_url == onclose){
                window.location.reload();
            }else{
                window.location.href = onclose;
            }
        }
    });

}

function showLoader(){
    $("#id_overlay").fadeIn();
    $("#id_load").fadeIn();
}

function hideLoader(){
    $("#id_load").fadeOut();
    $("#id_overlay").fadeOut();
}

function GetReference(idx){
    // showLoader();
    $.ajax({
        url: $("input[name=roundone-get-reference]").val(),
        type: "post",
        data: $("#id_"+idx).serialize(),

        success: function(response){
            hideLoader();
            result = JSON.parse(response);
            if(result.status)
            {
                if(result.redirect && result.redirect_url.length > 0) 
                {
                    window.location.href = result.redirect_url;
                }
                else if(result.response == false)
                {
                    $("#api_rsp").modal('hide');
                    showErrorModal(result.message, "Ok");
                }
                else if(result.response == false && result.message == "Education incomplete")
                {
                   $("#api_rsp").modal('hide');
                   showErrorModal(result.message, "", "Complete Profile", "", "/dashboard/roundone/profile/");
                }
                else
                {
                    showSuccessModal(result.message, "Ok");
                }
            }
            else
            {
                $("#api_rsp").modal('hide');
                showErrorModal(result.message, "Ok", "Cancel");
            }
        },
        failure: function(response){
            showErrorModal("Error referring for this job", "Ok", "Cancel");
        },
        complete: function(response){
            hideLoader();
        }
    });
}

function onClickGetReference(idx){
    console.log(idx);
    question = "Do you want to edit profile before applying?"
    $("#id_success_accept").unbind("click");
    $("#id_success_reject").unbind("click");
    $("#api_rsp").modal('show');
    $("#id_success_message").html(question);
    $("#id_success_accept").show();
    $("#id_success_reject").show();
    $("#id_success_accept").html("Apply");
    $("#id_success_reject").html("Edit Profile");
    
    // clicking apply
    $("#id_success_accept").on("click", function(){
        $("#id_success_modal").modal('hide');
        GetReference(idx);
    });

    // Clicking Editing Profile
    $("#id_success_reject").on("click", function(){
        $("#id_success_modal").modal('hide');
        showLoader();
        $.ajax({
            url: $("input[name=roundone-redirect-profile]").val(),
            type: "post",
            data: $("#id_"+idx).serialize(),
            success: function(response){
                result = JSON.parse(response)
                if(result.redirect){
                    window.location.href = result.redirect_url;
                }else{
                    window.location.href = "/dashboard/roundone/profile/";
                }
                hideLoader();
            },
            failure: function(response){
                showErrorModal("Error referring for this job", "Ok", "Cancel");
            },
            complete: function(response){
                hideLoader();
            }

        });
    });
}

$("#id_close_success_modal").on("click", function(){
    $("#id_success_modal").hide("slow");
});

$("#success_overlay_div").on("click", function(){
    $("#id_success_modal").hide("slow");
});

$("#id_close_error_modal").on("click", function(){
    $("#id_error_modal").hide("slow");
});

$("#error_overlay_div").on("click", function(){
    $("#id_error_modal").hide("slow");
});
