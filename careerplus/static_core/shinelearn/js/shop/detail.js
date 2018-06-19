var showChar = 280 ;  // How many characters are shown by default
var ellipsestext = "..." ;
var moretext = " know more" ;
var lesstext = " know less" ;

function showMoreLess(){
  // Configure/customize these variables.

  $('.more').each(function() {
    var content = $(this).html();

    if(content.length > showChar) {

        var c = content.substr(0, showChar);
        var h = content.substr(showChar, content.length - showChar);
        var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="#" class="morelink" style="display:inline-block;">' + moretext + '</a></span>';


        $(this).html(html);
    }

  });

};

$(document).ready(function () {

  // $(window).on('load',function(){
  //   $('#login-model').modal('show');
  // });

  // $(document).on("click", "#login-now-button", function() {
  //   $('#login-model').modal('show');
  // });


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


    $(document).on("click", ".other-product", function() {
      var data_pk = $(this).attr('data-id');
      var main_pk = $(this).attr('main-id');

      data = "?main_pk="+ main_pk + "&obj_pk=" + data_pk;
      $.ajax({
        url: "/shop/product/content-by-ajax/" + data,
        type: "GET",
        dataType: "json",
        success: function(data) {
          // console.log("success");
          if (data.status == 1 ){
            currentUrl = top.window.location.pathname;
            $("#id-detail-body").empty();
            $('#id-detail-body').html(data.detail_content);
            if (typeof (history.pushState) != "undefined") {
              // console.log('hello');
              // console.log(data.url);
              // console.log(data.title);
              var obj = { Title: data.title, Url: data.url };
              history.pushState(obj, obj.Title, obj.Url);
              document.title = data.title;
            }
            checkedInitialRequired();
            updateCartPrice();
            showMoreLess();
            $('.cls_scroller').scrollerdiv();
            $('.cls_sticky_scroller').productdetailAnimations();
            activeOnScroll.init({ className:'.cls_scroll_tab'});
          }
        },
        failure: function(response){
          console.log("failure");
        }
      });

    });


    $(document).on("click", ".review-load-more", function() {
   
           LoadMoreProductReview($(this).attr('data-product'));
      });

    
    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $("input[name=country_code]").val(); //$('#call_back_country_code-id').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });
    
    

  $(document).on('click', '#id_callback', function() {
    $('#callback_form').validate({
      rules:{
        name:{
          required: true,
            maxlength: 80,
        },
        number:{
            required: true,
            number: true,
            indiaMobile: true,
            // minlength: 4,
            maxlength: 10
        },
        msg:{
          required: true,
          maxlength: 500,
        },
        email:{
          required: true,
          maxlength: 100,
          email: true,
        }
      },
      messages:{
        name:{
          required: "Name is Mandatory.",
          maxlength: "Maximum 80 characters.",
        },
        email:{
          required: "Email is Mandatory.",
          maxlength: "Please enter at most 100 characters.",
          email: "Please enter valid email"
        },
        number:{
          required: "Mobile Number is Mandatory",
          number: "Enter only number",
          indiaMobile: "Please enter 10 digits only",
          maxlength: "Please enter 10 digits",
          // minlength: "Please enter atleast 4 digits"
        }, 
      },
      highlight:function(element, errorClass) {
          $(element).closest('.form-group').addClass('error');
      },
      unhighlight:function(element, errorClass) {
          $(element).closest('.form-group').removeClass('error');
          $(element).siblings('.error-txt').html('');      
      },
      errorPlacement: function(error, element){
          $(element).siblings('.error-txt').html(error.text());
      },
      ignore : '',
      submitHandler: function(form){
        // ga code
        var path = window.location.pathname, 
            action = '';
        if (path.indexOf('/course/') > -1) {
          action = 'Course Enquiry';
        } else if (path.indexOf('/services/') > -1) {
          action = 'Service Enquiry';
        }
        MyGA.SendEvent('QueryForm', 'Form Interactions', action, 'success');
        //form.submit();
        var formData = $(form).serialize();
        $.ajax({
          url : "/lead/lead-management/",
          type: "POST",
          data : formData,
          success: function(data, textStatus, jqXHR)
          {
            alert('Your Query Submitted Successfully.');
            $("#detailpage").modal('toggle');
            form.reset();
          },
          error: function (jqXHR, textStatus, errorThrown)
          {
            alert('Oops Some error has occured. Kindly try again later.');
            $("#detailpage").modal('toggle');
            form.reset();
          }
        });
      }
    });

    var flag = $('#callback_form').valid();
    if (flag){
      $('#callback_form').submit();}
  });

  // scroll effect;
  activeOnScroll.init({ className:'.cls_scroll_tab'});
});
    $(document).ready(function() {
      showMoreLess();

      $(document).on('click', '.morelink', function(e){
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

      // $('.about-tab a').click(function(){
      //   $('.about-tab a').removeClass('active');
      //   $(this).addClass('active');
      // });

      $(document).on('click', '.cls_scroll_tab', function(e){
        e.preventDefault();
        e.stopPropagation();
        var target = $(e.target);
        if(target.hasClass('cls_tab_child')){
          $('html,body').animate({scrollTop : $(''+target.attr('href')).offset().top - target.outerHeight() - $('#id_nav').outerHeight()},1000);
        }
      });
      
      function getUrlVar(key){
        var result = new RegExp(key + "=([^&]*)", "i").exec(window.location.search); 
        return result && unescape(result[1]) || ""; 
      }
      var res = getUrlVar('query');
      if (res == 'True')
      {
        $('#detailpage').modal('show');
      }
        
  });
          
