window.fbAsyncInit = function() {
        FB.init({
          appId  : '1482454715170390', // App ID
          status : true, // check login status
          cookie : true, // enable cookies to allow the server to access the session
          xfbml  : true , // parse XFBML
          version: 'v2.10',
        });
    };
    
    function Login()
    {
        FB.login(function(response) {
           if (response.status == 'connected')
               {
                    var accessToken = response.authResponse.accessToken;
                    var expiresIn = response.authResponse.expiresIn;
                    window.location.href = '/user/social/login/?accessToken='+accessToken+'&expiresIn='+expiresIn+'&key=fb';
                    console.log(response);
               } 
            else 
                {
                 console.log('User cancelled login or did not fully authorize.');
                }
        },{scope: 'email'});
     }
    // Load the SDK asynchronously
    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.10&appId=1482454715170390";
            fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
    
    // Social Gplus Login

    function loginCallback(result)
    {

        if(result['status']['signed_in'])
            {
                console.log(result);
                var access_token = result.access_token
                var expiresIn = result.expires_in
                window.location.href = '/user/social/login/?accessToken='+access_token+'&expiresIn='+expiresIn+'&key=gplus';
            }   
    }


    function glogin() 
    {
        var myParams = {
            'clientid' : '653414155457-ufec3m78n4ctcvfqn34jf8skn4mv909e.apps.googleusercontent.com',
            'cookiepolicy' : 'single_host_origin',
            'callback' : 'loginCallback', //callback function
            'approvalprompt':'force',
            'scope' : 'profile email',
        };
        gapi.auth.signIn(myParams);
    }

    var auth2;
    var startApp = function() {
        gapi.load('auth2', function(){
            /* Retrieve the singleton for the GoogleAuth library and set up the client.*/
            auth2 = gapi.auth2.init({
                client_id: '653414155457-ufec3m78n4ctcvfqn34jf8skn4mv909e.apps.googleusercontent.com',
                cookiepolicy: 'single_host_origin',
                /* Request scopes in addition to 'profile' and 'email'*/
                scope: 'profile email'
            });
        });
    };

    (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; 
       po.async = true;
       po.src = 'https://apis.google.com/js/client.js?onload=startApp';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();

$(document).ready(function() {
    // login and registration js 
    var emailresponse;
    $.validator.addMethod("emailDoesNotExist",
        function(value, element) {
            $.ajax({
                type: "GET",
                async: false,
                url:"/ajax/email-exist/",
                data:{email:$("#id_email").val()},
                success: function(res)
                {
                    emailresponse = res.exists;
                }
            });
             return emailresponse;

        },
        "This email id does not exists."
    );
    $("#login_form").validate({
        submitHandler: function(form) {
            // e.preventDefault();
            if($(this).val() != '')
            {
              $('button[type="submit"]').prop('disabled', false);  
            }
            else
            {
              $('button[type="submit"]').prop('disabled', true);
            }   
        },
        rules: {
                email:{
                    required:true,
                    email:true,
                    emailDoesNotExist:true

                },
                password:{
                    required:true,
                    minlength:6,
                    maxlength: 15
                }
        },
        messages:{
            email: { required:"Please enter a valid email address"},
            password:{
                required: "Please provide a password"
            }
        }
    });

    $("#forgot_form").validate({
        submitHandler: function(form) {
            var formData = $(form).serialize();
            var post_url = $(form).attr('action' );
            $('#forgot_div').modal('hide');
            $.ajax({
                url: post_url,
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(json) {
                    $("#forgot_form")[0].reset();
                    if (json.exist == true){
                        alert('Link has been sent to your registered email id');
                        // $("#msg_for_user").html("Link has been sent to your registered email id").show();
                        // $('#forgot_div').modal('show');
                    }
                    else if (json.notexist == true){
                        $("#msg_for_user").html("your email does not exist on shine learning").show();
                        $('#forgot_div').modal('show');
                    }
                    else if (json.noresponse == true){
                        $("#msg_for_user").html("Something went wrong. Try again later").show();
                        $('#forgot_div').modal('show');           
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
    // end login and registration js

    $('#modalforgot').click(function() {
        $('#forgot_div').modal('show');
        $("label#id_email-error.error").remove();
        $("#msg_for_user").hide();
    });
});