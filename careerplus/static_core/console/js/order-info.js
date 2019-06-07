
function order_get_details(o_id,key,element){

    btn = event.target;
     btn.setAttribute('disabled',true);
    if(o_id != "undefined"){
    $.ajax({
    url: "/api/v1/order-detail/" + o_id,
    type: "GET",
    data: {
           "fl":key
    },
    dataType: "json",
    success: function(data,textStatus, jqXHR) {
     btn.setAttribute('disabled',true);
    $('#'+element+'_field'+ o_id).text("");
    for (key in data){
    $('#'+element+'_field' + o_id).append(key+'- '+data[key] + '</br>');
    }
    },
    error: function(xhr, ajaxOptions, thrownError) {
        if (xhr.status !=200){
      $('#'+element+'_field'+ o_id).text("N.A");
       btn.removeAttr('disabled');


        }
    }

    });
    }
    else{
        alert("Something went wrong");
        btn.removeAttr('disabled');

    }
}