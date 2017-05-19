function addToCart(prod_id){
    console.log()
	if (prod_id){
        $('#id-cart-type').val("add_cart");
		var formData = $('#cartForm').serialize();
		$.ajax({
            url: '/cart/add-to-cart/',
            type: 'POST',
            data:formData,
            dataType: 'json',
            success: function(json) {

            	if (json.status == 1){
            		alert("product added in cart successfully");
            	}

            	else if (json.status == 0){
            		alert("product allready in cart.");
            		
            	}

            	else if (json.status == -1){
            		alert(json.error_message);
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

function removeFromCart(line_id){
    if (line_id){
        var formData = $('#cart_remove_form' + line_id).serialize();
        $.ajax({
            url: '/cart/remove-from-cart/',
            type: 'POST',
            data:formData,
            dataType: 'json',
            success: function(json) {
                if (json.status == 1){
                    alert("product removed from cart successfully");
                }

                else if (json.status == -1){
                    alert(json.error_message);
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


$(document).ready(function() {
     $('#enrol-now-button').click(function() {
        $('#id-cart-type').val("enrol_cart");
        var formData = $("#cartForm").serialize();
        console.log(formData);
        $.ajax({
            url : '/cart/add-to-cart/',
            type: 'POST',
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                console.log(data.status);
                if (data.status == 1){
                    console.log(data.redirect_url);
                    window.location.href = data.redirect_url
                    //window.location(data.redirect_url);
                }
                else if (data.status == -1){
                    alert(data.error_message);
                }
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert('Something went wrong. Try again later.');
            }
        });
    });
});
