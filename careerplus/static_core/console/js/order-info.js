
function order_get_details(o_id,key,element,counter='1'){

    btn = event.target;
     btn.setAttribute('disabled',true);
    if(o_id != "undefined"){

        $.ajax({
            url: "/api/v1/order-detail/" + o_id + "/",
            type: "GET",
            data: {
                   "fl":key
            },
            dataType: "json",
            success: function(data,textStatus, jqXHR) {
                btn.style.visibility= "hidden";
                $('#'+element+'_field'+ o_id+'_'+counter).text("");
                for (key in data){
                    $('#'+element+'_field' + o_id+'_'+counter).append(key+'- '+data[key] + '</br>');
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                if (xhr.status !=200){
                    $('#'+element+'_field'+ o_id+'_'+counter).text("N.A");
                    btn.removeAttr('disabled');
                    btn.style.visibility= "block";

                }
            }
        });
    }
    else{
        alert("Something went wrong");
        btn.removeAttr('disabled');

    }
}