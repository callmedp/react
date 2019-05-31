
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
    success: function(data) {
     btn.setAttribute('disabled',true);
    $('#'+element+'_field'+ o_id).text("");
    for (key in data){
    $('#'+element+'_field' + o_id).append(key+'- '+data[key] + '</br>');
    }
    },
    error: function(xhr, ajaxOptions, thrownError) {
        alert("Something went wrong. Try again later");
         btn.removeAttr('disabled');
    }

    });
    }
    else{
        alert("Something went wrong");
                 btn.removeAttr('disabled');

    }
}