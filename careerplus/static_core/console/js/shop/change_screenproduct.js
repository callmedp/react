$(document).ready(function() {
    var d = new Date();
    var todayDate = '' + d.getDate() + '-' + (d.getMonth() + 1) + '-' + d.getFullYear();

    function dateclass(el) {
      el.daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        minDate:todayDate,
        autoUpdateInput: false,
        locale: {
          format: 'DD-MM-YYYY'
        }
      }, function(chosen_date) {
        el.val(chosen_date.format('DD-MM-YYYY'));
      });
    }


    $('.batch_launch_date, .apply_last_date, .last_date_of_payment, .payment_deadline').each(function(){
      dateclass($(this));
    });
  $('.click-modal').click(function(){
    let msg = $(this).data("msg");
    $("#alertModalOk").data("action", msg);
    if (msg == "approval"){
      let message = 'Please make sure you have saved your changes. Do you wish to send this for approval?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "revert"){
      let message = 'Do you want to revert all changes?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
  }
    else if(msg == "live"){
      let message = 'Do you want to copy data to live?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "reject"){
      let message = 'Do you reject the changes?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
     
  });
  var processing = true;
  $('#alertModalOk').click(function(){
    let msg = $(this).data("action");
    let form = $('#approval-form');
    let action = form.find("input[name='action']");
    action.val(msg);
    if (processing){
      processing = false;
    $.ajax({
      url: '/console/screenproduct/action/' + msg +'/',
      type: 'post',
      data: form.serialize(),
      dataType: 'json',
      success: function(json) {
          processing = false;
          if (json['error']) {
            window.location.reload();
          }
          if (json['success']) {
            window.location.href = json['next_url'];
          }
      },
      failure: function(response){
          alert("Something went wrong, Please try again")
          processing = true;
      },
      error: function(xhr, ajaxOptions, thrownError) {
          alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);
          processing = true;
      }
    });
  }else{
    $("#alertModal").find('#alertModalBody').html("One request is already processing");
  };
  });


});