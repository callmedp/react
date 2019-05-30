
function order_get_details(o_id,key,element){
    if(o_id != "undefined"){
    $.ajax({
    url: "/api/v1/order-detail/" + o_id,
    type: "GET",
    data: {
           "fl":key
    },
    dataType: "json",
    success: function(data) {
    $('#'+element+'_field'+ o_id).text("");
    for (key in data){
    $('#'+element+'_field' + o_id).append(key+'- '+data[key] + '</br>');
    }
    },
    error: function(xhr, ajaxOptions, thrownError) {
        alert("Something went wrong. Try again later");
    }

    });
    }
    else{
        console.log("error  ");
    }
}