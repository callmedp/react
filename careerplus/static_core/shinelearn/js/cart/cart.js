// function addToCart(prod_id){
//     console.log()
// 	if (prod_id){
//         $('#id-cart-type').val("add_cart");
// 		var formData = $('#cartForm').serialize();
// 		$.ajax({
//             url: '/cart/add-to-cart/',
//             type: 'POST',
//             data:formData,
//             dataType: 'json',
//             success: function(json) {

//             	if (json.status == 1){
//             		alert("product added in cart successfully");
//             	}

//             	else if (json.status == 0){
//             		alert("product allready in cart.");
            		
//             	}

//             	else if (json.status == -1){
//             		alert(json.error_message);
//             	}
//             },
//             failure: function(response){
//                 alert("Something went wrong, Please try again")
//             },
//             error: function(xhr, ajaxOptions, thrownError) {
//                 alert("Something went wrong, Please try again")
//             }
//         });
// 	}

// };

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


$(document).ready(function() {

    // $('#enrol-now-button').click(function() {
    //     $('#id-cart-type').val("enrol_cart");
    //     var formData = $("#cartForm").serialize();
    //     console.log(formData);
    //     $.ajax({
    //         url : '/cart/add-to-cart/',
    //         type: 'POST',
    //         data : formData,
    //         success: function(data, textStatus, jqXHR)
    //         {
    //             console.log(data.status);
    //             if (data.status == 1){
    //                 console.log(data.redirect_url);
    //                 window.location.href = data.redirect_url
    //                 //window.location(data.redirect_url);
    //             }
    //             else if (data.status == -1){
    //                 alert(data.error_message);
    //             }
    //         },
    //         error: function (jqXHR, textStatus, errorThrown)
    //         {
    //             alert('Something went wrong. Try again later.');
    //         }
    //     });
    // });



    $('input[name="radio"]').click(function(){
        if ($(this).is(':checked'))
        {
            var var_price =  parseFloat($(this).attr('data-price'));
            var var_id = $(this).attr('data-id');
            var_price = 'Rs. ' + var_price.toString() + '/-';
            $('#total-price').text(var_price);
            $('#total-price').attr("sum-price", var_price);
        }
    });


    $('input[name="fbt"]').click(function(){
        if ($(this).is(':checked'))
        {
            var fbt_price =  parseFloat($(this).attr('data-price'));
            var sum_price = parseFloat($('#total-price').attr('sum-price'));
            sum_price = fbt_price + sum_price;
            show_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#total-price').text(show_price);
            $("#total-price").attr("sum-price", sum_price);
        }
        else{
            var fbt_price =  parseFloat($(this).attr('data-price'));
            var sum_price = parseFloat($('#total-price').attr('sum-price'));
            sum_price = sum_price - fbt_price;
            show_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#total-price').text(show_price);
            $("#total-price").attr("sum-price", sum_price);

        }
    });

    $('input[name="required_option"]').click(function(){
        if ($(this).is(':checked'))
        {
            var req_price =  parseFloat($(this).attr('data-price'));
            var sum_price = parseFloat($('#total-price').attr('sum-price'));
            sum_price = req_price + sum_price;
            show_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#total-price').text(show_price);
            $("#total-price").attr("sum-price", sum_price);
        }
        else{
            var req_price =  parseFloat($(this).attr('data-price'));
            var sum_price = parseFloat($('#total-price').attr('sum-price'));
            sum_price = sum_price - req_price;
            show_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#total-price').text(show_price);
            $("#total-price").attr("sum-price", sum_price);

        }
    });


    $('#add-to-cart').click(function() {
        var prod_id = $('#add-to-cart').attr('prod-id');
        // required options ie. for countries and product varification

        var req_options = [];
        if ($('input[name="required_option"]').length){
            $('input[name="required_option"]').each(function(){
                if ($(this).is(':checked'))
                {
                    req_options.push($(this).attr('data-id'));
                }
            });

            if (!req_options.length){
                $('#error_required').text('*Please select options')
                prod_id = 0
            }
        }

        if (prod_id){

            var cart_type = "cart";
            var fbt = [];
            // frequently  bought together
            $('input[name="fbt"]').each(function () {
                if ($(this).is(':checked')){
                    if ($(this).attr('data-id')){
                        fbt.push($(this).attr('data-id'));
                    }
                }
            });

            // courses variations
            var cv_id;
            $('input[name="radio"]').each(function(){
                if ($(this).is(':checked'))
                {
                    cv_id = $(this).attr('data-id');
                }
            });


            data = {
                "prod_id": prod_id,
                "addons": fbt,
                "cart_type": cart_type,
                "cv_id": cv_id,
                "req_options": req_options,
            }

            $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function(json) {

                    if (json.status == 1){
                        alert("product added in cart successfully");
                    }

                    else if (json.status == -1){
                        alert("Something went wrong, Please try again.")
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

    });


    $('#enrol-now-button').click(function() {
        var prod_id = $('#enrol-now-button').attr('prod-id');

        var req_options = [];
        if ($('input[name="required_option"]').length){
            $('input[name="required_option"]').each(function(){
                if ($(this).is(':checked'))
                {
                    req_options.push($(this).attr('data-id'));
                }
            });

            if (!req_options.length){
                $('#error_required').text('*Please select options')
                prod_id = 0
            }
        }

        if (prod_id){

            var cart_type = "express";
            var fbt = [];
            // frequently  bought together
            $('input[name="fbt"]').each(function () {
                if ($(this).is(':checked')){
                    if ($(this).attr('data-id')){
                        fbt.push($(this).attr('data-id'));
                    }
                }
            });

            // courses variations
            var cv_id;
            $('input[name="radio"]').each(function(){
                if ($(this).is(':checked'))
                {
                    cv_id = $(this).attr('data-id');
                }
            });

            // console.log(prod_id);

            data = {
                "prod_id": prod_id,
                "addons": fbt,
                "cart_type": cart_type,
                "cv_id": cv_id,
                "req_options": req_options,
            }

            $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function(data, textStatus, jqXHR) {

                    if (data.status == 1){
                        window.location.href = data.redirect_url
                    }
                    else if (data.status == -1){
                        alert(data.error_message);
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

    });



});
