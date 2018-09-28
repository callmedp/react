$(document).ready(function() {
  $('.click-modal').click(function(){
    let msg = $(this).data("msg");
    $("#alertModalOk").data("action", msg);
    if (msg == "active"){
      let message = 'Please make sure you have saved your changes. Do you wish to make this category active?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "inactive"){
      let message = 'Do you want to make this category inactive?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "skill"){
      let message = 'Do you want to make skillpage of this category?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "noskill"){
      let message = 'Do you want to make remove skillpage of this category?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "service"){
      let message = 'Do you want to make service page of this category?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "noservice"){
      let message = 'Do you want to make remove service page of this category?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }

    else if(msg == "university"){
      let message = 'Do you want to make university page of this category?';
      $("#alertModal").modal('show').find('#alertModalBody').html(message);
    }
    else if(msg == "nouniversity"){
      let message = 'Do you want to remove university page of this category?';
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
      url: '/console/category/action/' + msg +'/',
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