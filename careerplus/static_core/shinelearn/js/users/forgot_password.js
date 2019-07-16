$(document).ready(function() {
    $("#forgot_form").validate({
        submitHandler: function(form) {

            var formData = $(form).serialize();
            var post_url = $(form).attr('action' );
            $.ajax({
                url: post_url,
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(json) {

                    $("#forgot_form")[0].reset();
                    if (json.exist == true){
                        alert("Link has been sent to your registered email id");
                        if (json.next != '')
                        {window.location.href = json.next;}
                    }
                    else if (json.notexist == true){
                        alert("your email does not exist on shine learning");
                    }
                    else if (json.noresponse == true){
                        alert("Something went wrong. Try again later");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                }
            });
        },
        rules: {
            email:{
                required:true,
                email:true,
            }
        },
        messages:{
            email: { required:"Please enter a valid email address"},
        }
    });
});