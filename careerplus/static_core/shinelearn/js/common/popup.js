function disableScroll() {
    // Get the current page scroll position
    scrollTop =
      window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft =
      window.pageXOffset || document.documentElement.scrollLeft,
        window.onscroll = function() {
            window.scrollTo(scrollLeft, scrollTop);
        };
}
function enableScroll() {
    window.onscroll = function() {};
}

var modal = document.getElementById("popup_subscribe");
var span = document.getElementsByClassName("close_popup_modal")[0];
span.onclick = function() {
    modal.style.display = "none";
    enableScroll();
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        enableScroll();
    }
}
$(document).ready(function() {
  setTimeout(function() {
      modal.style.display = "block";
      disableScroll();
  }, 10000);
});
