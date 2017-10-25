 var processing = false;
  
function LoadMoreProductReview(pv_id) {
      if (processing) {
          return false;
      }
      else{    
        if (pv_id) {
          try{
            let page, elem;
            elem = document.getElementById("id_review_page");
            try {
                elem.value = parseInt(elem.value) + 1;
            } catch (_error) {
              i = _error;
              elem.value = 2;
            }
            page = document.getElementById("id_review_page").value;
            processing = true;
            
            $.ajax({
                url: '/shop/reviews/' + encodeURIComponent(pv_id) + '/?pg=' + encodeURIComponent(page),
                dataType: 'html',
                success: function(html) {
                    $('#loadmorereviewbtn').remove();
                    
                    $('#id_review_list').append(html);
                    
               },
               complete: function(response){
                    return processing = false;
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);
                }
            });
        }
        catch(e){
          alert("Invalid Page");
        }
        }
      }
    };


$(document).ready(function () {

    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $("input[name=country_code]").val(); //$('#call_back_country_code-id').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });
    $('#callback_form').validate({
        rules:{
                name:{
                  required: true,
                    maxlength: 80,
                },
                mobile:{
                    required: true,
                    number: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15
                },
                message:{
                  required: true,
                  maxlength: 500,
                },
            },
        messages:{
            name:{
              required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters.",
            },
            mobile:{
                required: "Mobile Number is Mandatory",
                number: "Enter only number",
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter less than 16 digits",
                minlength: "Please enter atleast 4 digits"
            },
            
        },
        highlight:function(element, errorClass) {
            $(element).siblings('.error').removeClass('hide_error'); 
        },
        unhighlight:function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error');    
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error').html(error.text());
        } 
  });

  
  $('#id_callback').click(function(){
    if ( $("#callback_form").valid()) {
      var formData = $("#callback_form").serialize();
      $.ajax({
              url : "/shop/crm/lead/",
              type: "POST",
              data : formData,
              success: function(data, textStatus, jqXHR)
              {
                $("#detailpage").modal('hide');
                alert('Your Query Submitted Successfully.');
                    window.location.reload();
              },
              error: function (jqXHR, textStatus, errorThrown)
              {
                  window.location.reload(); 
              }
          }); 
    }  
    });
});
      $(document).ready(function() {
      // Configure/customize these variables.
      var showChar = 280;  // How many characters are shown by default
      var ellipsestext = "...";
      var moretext = " know more";
      var lesstext = " know less";
      

      $('.more').each(function() {
          var content = $(this).html();
   
          if(content.length > showChar) {
   
              var c = content.substr(0, showChar);
              var h = content.substr(showChar, content.length - showChar);
   
              var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink" style="display:inline-block;">' + moretext + '</a></span>';
   
              $(this).html(html);
          }
   
      });
   
      $(".morelink").click(function(){
          if($(this).hasClass("less")) {
              $(this).removeClass("less");
              $(this).html(moretext);
          } else {
              $(this).addClass("less");
              $(this).html(lesstext);
          }
          $(this).parent().prev().toggle();
          $(this).prev().toggle();
          return false;
      });
      $('.about-tab a').click(function(){
        $('.about-tab a').removeClass('active');
        $(this).addClass('active');
      });
        
  });
    