$.validator.addMethod("extn", function(value, element) {
    var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
    if(value && !allowedExtensions.exec(value)){
        return false;
    }
    else{
        return true;
    }
        
});

$.validator.addMethod("custom_comment",
    function(value, element) {
        if($('#reject-reason').val() && $('#reject-reason').val().trim()){
            return true;
        }
        return false;
});


function mobileRejectService(oi_pk) {
    $("#reject-form-id" + oi_pk).validate({
        rules: {
            comment:{
                required: function(){
                    if($('#uploadBtn').val() == "")
                        return true;
                    else
                        return false;
                },
                custom_comment: true,

            } ,

            reject_file: {
                extn: true,
            }
        },
        messages: {
            comment:{
                required: 'This field is required',
                custom_comment: 'This field is required',
            },
            reject_file: 'only pdf, doc and docx formats are allowed',
        },
        submitHandler: function(form) {                
            return false;
        },

    });

    var flag = $('#reject-form-id' + oi_pk).valid();
    if (flag){
        var formData = new FormData($('#reject-form-id' + oi_pk)[0]);
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
                $('#reject-form-id' + oi_pk)[0].reset();
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });

    }   
};

function mobileAccept(oi_pk){
    if (oi_pk){
        var formData = $('#mobileaccept-form' + oi_pk).serialize();
        console.log(formData);
        $.ajax({
            url: '/dashboard/inbox-acceptservice/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(data) {
                $('.modal').hide();
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
                window.location.reload();
            }
        });
    }
}

function openPopup(el) {
    $('.modal').hide();
    $('#' + el).fadeIn(200);   
}

function closePopup() {
    $('.modal').fadeOut(300);
}

let  getCookie = (name)=> {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

const uploadResumeShineMobile = (checkbox,order_id)=>{
    let request = fetch(`/api/v1/order/${order_id}/update/`,{
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        method: 'PATCH',  
        body: JSON.stringify({
                    service_resume_upload_shine: $(checkbox).is(':checked')
                }),
    });

    request.then((resp) =>resp.json())
    .then(response => {
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


let pause_resume_api_hit_once_mobile = false

const pause_resume_service_mobile = (el,oi_id,oi_status)=>{
    if (pause_resume_api_hit_once_mobile)
        return

    pause_resume_api_hit_once_mobile = true
    
    let request = fetch(`/api/v1/order/orderitem/${oi_id}/update/`,{
        headers: {
            "Content-Type": "application/json"
        },
        method: 'PATCH',  
        body: JSON.stringify({
                    oi_status
                }),
    });

    request.then((resp) =>resp.json())
    .then(response => {
        error = response['oi_status'] !== oi_status ? true : false
        title = error ? `Please wait 24 hours before ${oi_status==34 ? 'pausing' : 'resuming'} ` : 
                            response['oi_status'] ===34 ? 'Service is Paused' : 'Service is Resumed'
        Toast.fire({
                    type: error ?'error' : 'success',
                    title
        })
        location.reload()
    })
    .catch(e =>{
        Toast.fire({
            type: 'error',
            title:'Something went wrong'
        })
    })
}