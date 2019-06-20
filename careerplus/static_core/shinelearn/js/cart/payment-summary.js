function toggler(divId, show_hide_coupon) {
  if(show_hide_coupon){
      var ele = $("#show_hide_coupon")
      var text = ele.text()
      if(text == 'Apply coupon'){
        ele.text('Hide Coupon')
      }
      else {
        ele.text('Apply coupon')
       }
   }
  $("#" + divId).toggle();
}

function JSApplyDiscount() {
  var alert_message = '';
  if ($('#discount_code').val().trim()){
    $('#discount_code').parent().removeClass('error');
      try {
          var discount_code = $('#discount_code').val().trim();
          $.ajax({
              url: '/cart/applycoupon/',
              type: 'post',
              data: 'code=' + discount_code,
              dataType: 'json',
              success: function(json) {
                window.location.reload();
              },
              failure: function(response){
                  alert_message = 'Something is not working, Please try later!';
                  $('#discount_code').parent().addClass('error');
                  $('#discount-alert').empty();
                  $('#discount-alert').text(alert_message);
                  $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                  
              },
              error: function (result, status, err) {
                if(result && result.status == 400)
                {
                  alert_message = result.responseJSON;
                  alert_message = alert_message.error;
                }
                else{
                  alert_message = 'Something is not working, Please try later!';
                
                }
                $('#discount_code').parent().addClass('error');
                $('#discount-alert').empty();
                $('#discount-alert').text(alert_message);
                $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                
              }
          });
      }
      catch (e) {
        alert_message = 'Something is not working, Please try later!';
        $('#discount_code').parent().addClass('error');
        $('#discount-alert').empty();
        $('#discount-alert').text(alert_message);
        $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
        
      }
          
  }
  else{
      alert_message = 'Enter Discount Code First!';
      $('#discount_code').parent().addClass('error');
      $('#discount-alert').empty();
      $('#discount-alert').text(alert_message);
      $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
      
  }
};

function JSApplyPoint() {
  var alert_message = '';
  debugger
  if ($('#loyalty_point').val().trim()){
    $('#loyalty_point').parent().removeClass('error');
      try {
          var loyalty_point = $('#loyalty_point').val().trim();
          if(isNaN(loyalty_point)){
            throw "NaN"
          }
          loyalty_point = parseInt(loyalty_point, 10);
          var min_point = parseInt($('#loyalty_point').prop('min'), 10);
          var max_point = parseInt($('#loyalty_point').prop('max'), 10);
          if(loyalty_point <= min_point){
            throw "Min"
          }
          if(loyalty_point > max_point){
            throw "Max"
          }
          $.ajax({
              url: '/cart/applypoint/',
              type: 'post',
              data: 'point=' + loyalty_point,
              dataType: 'json',
              success: function(json) {
                window.location.reload();
              },
              failure: function(response){
                alert_message = 'Something is not working, Please try later!';
                $('#loyalty_point').parent().addClass('error');
                $('#point-alert').empty();
                $('#point-alert').text(alert_message);
                $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
              },
              error: function (result, status, err) {
                if(result && result.status == 400)
                {
                  alert_message = result.responseJSON;
                  alert_message = alert_message.error;
                }
                else{
                  alert_message = 'Something is not working, Please try later!';
                }
                $('#loyalty_point').parent().addClass('error');
                $('#point-alert').empty();
                $('#point-alert').text(alert_message);
                $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
              }
          });
      }
      catch (e) {
        if(e == 'NaN'){
          alert_message = 'Please enter digits!';
        }
        else if(e == 'Min'){
          alert_message = 'Redeem points should be greater than 0!';
        }
        else if(e == 'Max'){
          alert_message = 'Redeem points should be less than available points!';
        }
        else{
          alert_message = 'Something is not working, Please try later!';
        }
        $('#loyalty_point').parent().addClass('error');
        $('#point-alert').empty();
        $('#point-alert').text(alert_message);
        $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
      }
          
  }
  else{
      alert_message = 'Enter Loyalty Point First!';
      $('#loyalty_point').parent().addClass('error');
      $('#point-alert').empty();
      $('#point-alert').text(alert_message);
      $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
      
  }
};
function JSRemoveDiscount() {
  $.ajax({
      url: '/cart/removecoupon/',
      type: 'post',
      dataType: 'json',
      success: function(json) {
          window.location.reload();
      },
      failure: function(response){
          alert_message = 'Something is not working, Please try later!';
          $('#discount_code').parent().addClass('error');
          $('#discount-alert').empty();
          $('#discount-alert').text(alert_message);
          $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
          
      },
      error: function (result, status, err) {
        if(result && result.status == 400)
        {
          alert_message = result.responseJSON;
          alert_message = alert_message.error;
        }
        else{
          alert_message = 'Something is not working, Please try later!';
        
        }
        $('#discount_code').parent().addClass('error');
        $('#discount-alert').empty();
        $('#discount-alert').text(alert_message);
        $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
        
      }
  });

};
function JSRemovePoint() {
  $.ajax({
      url: '/cart/removepoint/',
      type: 'post',
      dataType: 'json',
      success: function(json) {
          window.location.reload();
      },
      failure: function(response){
          alert_message = 'Something is not working, Please try later!';
          $('#loyalty_point').parent().addClass('error');
          $('#point-alert').empty();
          $('#point-alert').text(alert_message);
          $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
          
      },
      error: function (result, status, err) {
        if(result && result.status == 400)
        {
          alert_message = result.responseJSON;
          alert_message = alert_message.error;
        }
        else{
          alert_message = 'Something is not working, Please try later!';
        
        }
        $('#loyalty_point').parent().addClass('error');
        $('#point-alert').empty();
        $('#point-alert').text(alert_message);
        $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
        
      }
  });

};


$(document).ready(function() {

  $('#payment-summary-continue-id').click(function() {
    $('#payment-summary-continue-id').attr('disabled', true);
  });

});