function updateTextArea() {
        var allVals = [];
        $('#element_checked :checked').each(function() {
           allVals.push($(this).attr("id"));
        });
        $('#slected_country').text(allVals);
    }
jQuery(document).ready(function($){
        $(".accordion_example1").smk_Accordion({
            showIcon: true, //boolean
            animation: true, //boolean
            closeAble: true, //boolean
            slideSpeed: 200 //integer, miliseconds
        });
        updateTextArea();
      // Configure/customize these variables.
      var showChar = 280;  // How many characters are shown by default
      var ellipsestext = "...";
      var moretext = " know more";
      var lesstext = " know less";
      

      $('.more').each(function() {
          var content = $(this).html();
   
          if(content.length > showChar) {
   
              var c = content.substr(0, showChar);
              var h = content.substr(showChar, content.length - showChar);
   
              var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink" style="display:inline-block;">' + moretext + '</a></span>';
   
              $(this).html(html);
          }
   
      });
   
      $(".morelink").click(function(){
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