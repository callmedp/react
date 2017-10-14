function removeFromCartMobile(line_id){
    if (line_id){
        var formData = $('#cart_remove_form' + line_id).serialize();
        $.ajax({
            url: '/cart/mobile/remove-from-cart/',
            type: 'POST',
            data:formData,
            dataType: 'json',
            success: function(json) {
                if (json.status == 1){
                    window.location.reload();
                    //alert("product removed from cart successfully");
                }
                else if (json.status == -1){
                    alert('Something went wrong, Please try again.');
                }
            },
            failure: function(response){
                alert("Something went wrong, Please try again")
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again")
            }
        });
    }

};

function deliveryOptionUpdate(line_id){
    if (line_id){
        //var formData = $('#delivery-option-form' + line_id).serialize();
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", $('input[name="csrfmiddlewaretoken"]').val());
        formData.append("delivery_type", $('select[name="delivery_type"]').val());
        formData.append("lineid", $('input[name="lineid"]').val());
        $.ajax({
            url: '/cart/update-deliverytype/',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            async: false,
            enctype: "multipart/form-data",
            success: function(data, textStatus, jqXHR){
                if (data.total_cart_amount != -1 && data.delivery_charge != -1){
                    if (data.delivery_charge){
                        var text_str = '+ Rs. ' + data.delivery_charge.toString() + '/-';
                        $('#delivery-charge' + line_id).text(text_str);
                    }
                    else{
                        $('#delivery-charge' + line_id).text('');
                    }
                    $('#total-cart-amount-id').text(data.total_cart_amount);
                }
            },
            failure: function(response){
                alert("Something went wrong, Please try again")
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again")
            }
        });
    }
}