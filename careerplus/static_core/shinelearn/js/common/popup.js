try {
var span = document.getElementsByClassName("close_popup_modal")[0];
span.onclick = function() {
    $('#popup_subscribe').modal('toggle');
}

$(document).ready(function() {
  if(sessionStorage.getItem('popState') != 'shown'){
  setTimeout(function() {
      $("#popup_subscribe").modal('show');
  }, 60000);
  sessionStorage.setItem('popState','shown')
  }
});
}
catch(e) {
  
}

