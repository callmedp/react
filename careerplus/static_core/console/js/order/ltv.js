function load_json () {
  var ltv_list = [];
  $(".ltv-value").each(function() { 
    ltv_list.push($(this).attr('data-pk')); 
  });
  load_ltv({"order_list":ltv_list});
}
function dump_json (data) {
}
function load_ltv (data) {
  $.ajax({
    url: '/ajax/get-ltv/',
    type: 'post',
    data: data,
    dataType: "json",
    success: function(data){
        if(data.status == 1){
          $(".ltv-value").each(function() { 
            $(this).text("Rs."+data[$(this).attr('data-pk')]); 
          });
        }
        return
    },
    error: function (xhr, ajaxOptions, thrownError) {
        console.log(errorMsg = 'Ajax request failed: ' + xhr.responseText);
      }
  });
}
    
    

$(document).ready(function() {
    load_json();

});