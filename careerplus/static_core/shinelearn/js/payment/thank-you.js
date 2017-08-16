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

	$(document).on('click', '#resume-sumbmit-button', function () {
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

        if (flag){
            $('#upload-order-resume-form').submit();
        }
        
    });
});