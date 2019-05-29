$(function(){
  
$("#loginform").validate({
      rules:{
          username:{
                  required:true,
                  maxlength: 60,
              },
          password:{
                  required:true,
                  maxlength: 20,
              },
              
          },
      messages:{
          username:{
                  required: "Please enter Username",
                  maxlength: "At most 60 characters"
              },
          password:{
                  required: "Please enter Password",
                  maxlength: "At most 20 characters"
              },
          
      },
      highlight:function(element, errorClass) {
           $(element).parent().addClass('login-error');
      },
      unhighlight:function(element, errorClass) {
          $(element).parent().removeClass('login-error');
      },
      errorPlacement: function(error, element) {
        element.siblings('.js-error').html(error.text());
       
     }

  });
});

function swapVisibleSection(){
  $("#forgot-password-section").toggle();
  $("#login-section").toggle();
}