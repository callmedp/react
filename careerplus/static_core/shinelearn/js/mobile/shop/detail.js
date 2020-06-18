function updateTextArea() {
        var allVals = [];
        $('#element_checked :checked').each(function() {
           allVals.push($(this).attr("id"));
        });
        $('#slected_country').text(allVals);
    }
jQuery(document).ready(function($){

      $("#done_click").click(function(){
          updateTextArea();
          $("#sidebar-countries").hide();
          $(".cls_mask").hide();
          $('body').css('overflow','auto');
      });
      $("#sidebar-countries-trigger").click(function(){
          $("#sidebar-countries").show();
      });

      $("#enquire_btn").on('click', function() {
        $('#enquire').addClass('show');
      });
      
      $("#back_btn").on('click', function() {
        $('#enquire').removeClass('show');
      });
  });

$("#feedback-form").validate({
  rules: {
      rating:{
          required: true,
      },
      review: {
          maxlength: 1500
      },
      title: {
          required: true,
      }
  },
  messages: {
      average_rating:{
          required: "rating is required."
      },
      review: {
          maxlength: "length should not be greater than 1500 characters.",
      },
      title: {
          maxlength: "length should not be greater than 20 characters."
      }
  },
  errorPlacement: function(error, element){
      $(element).siblings('small').find('.error').html(error.text());

  },
  submitHandler: function(form) {                
      return false;
  },

});

$(document).on('click', '[name="rating"]', function () {
    var flavour = $('[name="flavour"]').val();
    console.log(flavour);
    if (flavour == 'mobile'){
        var rating_val = $(this).attr('value');
        $('#selected-rating').text(rating_val);
    }
    else {
        var html = $(this).attr('value') + '<small>/5</small>';
        $('#selected-rating').html(html);
    }
    $('#rating-error').text('');
   
});

function feedback_submit (formData){

  var flag = $('#feedback-form').valid();
  var rating_flag = false;
  $('input[name="rating"]').each(function () {
      if ($(this).is(':checked')){
          rating_flag = true;
      }
  });
  if (!rating_flag){
      $('#rating-error').text('rating is mandatory');
  }
  if (flag && rating_flag){
    request_to_submit_feedback(formData)
  }
        
}

function request_to_submit_feedback(formData){
  $.ajax({
      url: '/shop/reviews/product/create/',
      type: 'POST',
      data : formData,
      dataType: 'json',
      success: function(json) {
          if (json.success){
            alert(json.display_message);
            window.location.reload();
          }
          else if(json.display_message){
            alert(json.display_message)
            refreshErrors(json)
          }
          else{
            refreshErrors(json)
          }
      },
      error: function(xhr, ajaxOptions, thrownError) {
          alert("Something went wrong, try again later");
      }
  });
}

function update_feedback_form(product_pk) {
  var formData = $('#feedback-form').serialize();
  $.ajax({
      url: '/shop/reviews/'+ product_pk + '/edit/',
      type: 'POST',
      data : formData,
      dataType: 'json',
      success: function(json) {
          if (json.success){
            alert(json.display_message);
            window.location.reload();
          }
          else if(json.display_message){
            alert(json.display_message)
            refreshErrors(json)
          }
          else{
            refreshErrors(json)
          }
      },
      error: function(xhr, ajaxOptions, thrownError) {
          alert("Something went wrong, try again later");
      }
  });
}

function submitReviewFromLocalStorage(){
  formData = localStorage.getItem("formData");
  if(formData){
    request_to_submit_feedback(formData);
    localStorage.removeItem("formData");
  }
  else{
    localStorage.removeItem("formData");
  }
}

function saveReviewFormDataToLocalStorage(){
    var formData = $('#feedback-form').serialize();
    if(formData) {
        localStorage.setItem('formData', formData );        
    }
}

function reviewLinkedInLogin() {
 
  saveReviewFormDataToLocalStorage()
  window.location.href= '/user/linkedin/code/?next=' + window.location.href
}
submitReviewFromLocalStorage()

function refreshErrors(json){
  var keys = ['review','title','rating']
  keys.forEach(function(element) {
    if(json[element]) {
      $('#'+element+'-error').text(json[element]);
    }
    else{
       $('#'+ element+'-error').text('');
    }
  });
}

function submit_feedback_form(is_logged_in) {
  if(is_logged_in=='True'){
    var formData = $('#feedback-form').serialize();
    feedback_submit(formData);
  }
  else {
    var flag = $('#feedback-form').valid();
    if(flag){
      $('.modal').hide();
      $('.modal').fadeIn(200);       
    }
  }
}

function closePopup() {
    $('#login-modal').modal('hide')
}

// handler for login through modal
$('#login-button').click(function() {
  flag = $("#login_form").valid();
  if (flag){
      var formData = $("#login_form").serialize();
      $('#login-button').prop('disabled', true);
      $.ajax({
          url : "/article/login-to-comment/",
          type: "POST",
          data : formData,
          success: function(data, textStatus, jqXHR)
          {
              console.log(data);
              if (data.response == 'login_user'){
                  var formData = $('#feedback-form').serialize();
                  feedback_submit(formData)
                  window.location.reload();
              }
              else if (data.response == 'error_pass'){
                  var error_message = data.error_message;
                  $('#non-field-error').text(error_message)
              }
              else if (data.response == 'form_validation_error'){
                  $('#non-field-error').text('Please enter Valid Data')
              }
              $('#login-button').prop('disabled', false);
          },
          error: function (jqXHR, textStatus, errorThrown)
          {
              alert('Something went wrong. Try again later.');
              $('#login-button').prop('disabled', false);
          }
      });
  }
});

$("#write_review_btn").click(function() {
  $("#write_review_container").slideToggle();
});

function openPopup() {
   
}

function closePopup() {
    $('.modal').fadeOut(300);
}


$('#redeem_test').click(function () {
  $('.overlay-background').show()
  $('body').addClass('body-noscroll')
  const prodId = $(this).attr('prod-id')
  createDirectOrder(parseInt(prodId) , 'assessment')
})




function createDirectOrder(productId, redeem_option) {

  $.ajax({
    url: '/api/v1/order/direct-order/',
    type: 'POST',
    data: { 'prod_id': productId, 'redeem_option': redeem_option },
    dataType: 'json',
    success: function (json) {
      if (json.status == 1) {
        window.location.href = json.redirectUrl;
      }
      else if (json.status == -1) {
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        alert("Something went wrong, Please try again.");
      }

    },
    failure: function (response) {
      alert("Something went wrong, Please try again");

    },
    error: function (xhr, ajaxOptions, thrownError) {
      alert("Something went wrong, Please try again");
    }
  });

}


