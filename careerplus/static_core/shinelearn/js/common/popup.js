var span = document.getElementsByClassName("close_popup_modal")[0];
span.onclick = function() {
    $('#popup_subscribe').modal('toggle');
}

$(document).ready(function() {
  setTimeout(function() {
      $("#popup_subscribe").modal('show');
  }, 10000);
});