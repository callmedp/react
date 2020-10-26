var modal = document.getElementById("popup_subscribe");
var span = document.getElementsByClassName("close_popup_modal")[0];
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
$(document).ready(function() {
  setTimeout(function() {
      modal.style.display = "block";
  }, 10000);
});
