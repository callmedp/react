function removeFromCartMobile(line_id) {
    if (line_id) {
        var formData = $('#cart_remove_form' + line_id).serialize();

        $.ajax({
            url: '/cart/mobile/remove-from-cart/',
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function (json) {
                if (json.status == 1) {
                    window.location.reload();
                    //alert("product removed from cart successfully");
                } else if (json.status == -1) {
                    alert('Something went wrong, Please try again.');
                }
            },
            failure: function (response) {
                alert("Something went wrong, Please try again")
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again")
            }
        });
    }

};

function handleDeliveryUpdation(formData, lineId,itemId) {
    $.ajax({
        url: '/cart/update-deliverytype/',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        async: false,
        enctype: "multipart/form-data",
        success: function (data, textStatus, jqXHR) {
            if (data.total_cart_amount != -1 && data.delivery_charge != -1) {
                let {
                    delivery_service_meta_desc: deliveryServiceDesc,
                    delivery_service_title: deliveryServiceTitle,
                    delivery_charge: deliveryCharge
                } = data;
                const str = `${deliveryServiceTitle}- ${Number(deliveryCharge) === 0 ? 'No extra cost' : 'Rs. ' + deliveryCharge.toFixed(2) + '/-'}`;
                $(`#active-delivery-title${lineId.trim()}`).text(str);

                $(`#active-delivery-description${lineId.trim()}`).text(`(${deliveryServiceDesc})`)

                if (data.delivery_charge) {
                    var text_str = '+ Rs. ' + data.delivery_charge.toString() + '/-';
                    $('#delivery-charge' + itemId).text(text_str);
                } else {
                    $('#delivery-charge' + itemId).text('');
                }

                const totalCartAmount = `Rs. ${data.total_cart_amount.toFixed(2).toString()}`;
                $('#total-cart-amount-id').text(totalCartAmount);

                const totalPayableAmount = `Rs. ${data.total_payable_amount.toFixed(2).toString()}`;
                $('#total-payable-amount').text(totalPayableAmount);
                const {sgst_amount: sgstAmount, cgst_amount: cgstAmount} = data
                // update sgst amount
                $('#sgst-amount').text(sgstAmount);
                // update cgst amountc
                $('#cgst-amount').text(cgstAmount);
        
            }

        },
        failure: function (response) {
            alert("Something went wrong, Please try again")
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Something went wrong, Please try again")
        }
    });
}

function deliveryOptionUpdate(line_id,itemId) {
    if (line_id) {
        //var formData = $('#delivery-option-form' + line_id).serialize();
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", $('input[name="csrfmiddlewaretoken"]').val());
        formData.append("delivery_type", $('select[name="delivery_type"]').val());
        formData.append("lineid", $('input[name="lineid"]').val());
        handleDeliveryUpdation(formData, line_id, itemId)
    }
}

const selectDeliveryType = (deliveryType, lineId, csrf,itemId) => {
    $(`#delivery-item${itemId}`).slideToggle(500,function (){
        if (lineId) {
            var formData = new FormData();
            formData.append("csrfmiddlewaretoken", csrf);
            formData.append("delivery_type", deliveryType);
            formData.append("lineid", lineId);
            handleDeliveryUpdation(formData, lineId,itemId);
        }
    });
    
}

const toggleDeliveryItems = (deliveryId) => {
    $(`#delivery-item${deliveryId}`).slideToggle();
    return false;
}

function cartScroller() {

};

$(document).ready(function ($) {

    if (window.CURRENT_FLAVOUR == 'mobile') {
        $(".accordion_example1").smk_Accordion({
            showIcon: true, //boolean
            animation: true, //boolean
            closeAble: true, //boolean
            slideSpeed: 200 //integer, miliseconds
        });
    }
    // Configure/customize these variables.
    var showChar = 280;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = " know more";
    var lesstext = " know less";


    $('.more').each(function () {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink" style="display:inline-block;">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });
    $(".morelink").click(function () {
        if ($(this).hasClass("less")) {
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
});
