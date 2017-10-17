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
        $('#action-type-id').val('upload_resume');
    });

    $(document).on('click', '#shine-resume-box', function () {
        $('#action-type-id').val('shine_reusme');
    });

    $(document).on('change', '#id-upload-resume', function () {
        var resume_name = $('#id-upload-resume')[0].files[0].name;
        $('#resume_name_id').text(resume_name);
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

                highlight: function(element) {
                    $('#id-upload-error').removeClass('hide-p');
                },
                unhighlight: function(element) {
                    $('#id-upload-error').addClass('hide-p');
                },
                errorPlacement: function(error, element){
                    // $(element).closest('ul').find(".error").html(error.text());
                    $('#id-upload-error').html(error.text());

                }
            });
            var flag = $('#upload-order-resume-form').valid();
        }
        else{
            flag = true
        }

        if (flag){
            console.log(action_type);
            $('#upload-order-resume-form')[0].submit();
        }
        
    });
});