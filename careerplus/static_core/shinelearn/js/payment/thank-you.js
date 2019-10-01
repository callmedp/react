$(document).ready(function() {

	$.validator.addMethod("extn", function(value, element) {
        var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
        if(value && !allowedExtensions.exec(value)){
            return false;
        }
        else{
            return true;
        }
            
    });

    $(document).on('click', '#upload-resume-box', function () {
        $('#upload-resume-box').removeClass('selected');
        $('#shine-resume-box').removeClass('selected');
        $('#upload-resume-box').addClass('selected');
        $('#action-type-id').val('upload_resume');
    });

    $(document).on('click', '#shine-resume-box', function () {
        $('#shine-resume-box').removeClass('selected');
        $('#upload-resume-box').removeClass('selected');
        $('#shine-resume-box').addClass('selected');
        $('#action-type-id').val('shine_reusme');
    });


	$(document).on('click', '#resume-sumbmit-button', function () {

        var action_type = $('#action-type-id').val();
        var flag = false;

        if (action_type == 'upload_resume'){
            $("#upload-order-resume-form").validate({
                rules: {
                    resume_file: {
                        required: true,
                        extn: true
                    },
                },
                messages: {
                    resume_file: {
                        required: 'This value is required',
                        extn: 'only pdf, doc and docx formats are allowed',
                    },
                },

            });
            var flag = $('#upload-order-resume-form').valid();
        }
        else{
            flag = true
        }

        if (flag){
            console.log(action_type);
            $('#upload-order-resume-form').submit();
        }
        
    });
});

const  getCookie = (name)=> {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }

$(document).ready(function(){
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });
    
})

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