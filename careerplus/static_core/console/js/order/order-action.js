function clickMarkPaidButton(order_id){
    if (order_id){
        $('#order-paid-form' + order_id).parsley().validate();
        if ($('#order-paid-form' + order_id).parsley().isValid()){
            /*$('#paidModalbody' + order_id).html('<div class="alert alert-success">Are you sure to mark paid order id=' + order_id + '?</div>');*/
            $('#markPaidActionId' + order_id).show();
            $('#paidmodal' + order_id).modal("show");
        }
    }
}


function markPaidOrder(order_id){
    if (order_id){
        var formData = $('#order-paid-form' + order_id).serialize();
        if($("#loader").length) {
            $("#loader").show()
        }
        $.ajax({
            url: '/ajax/order/markedpaid/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
                var msg = json.display_message;
                if($("#loader").length) {
                    $("#loader").hide()
                }
                if (json.status == 1){
                    alert(msg);
                    window.location.reload();
                }
                else{
                    alert(msg);
                     window.location.reload();
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
                 window.location.reload();
            }
        });
    }
}