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
  });