function addToCart(prod_id){
	if (prod_id){
		var formData = $('#addToCartForm').serialize();
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
                console.log(json.status);

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