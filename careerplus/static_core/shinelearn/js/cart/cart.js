
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

    $('input[name="radio"]').click(function(){
        if ($(this).is(':checked'))
        {
            var var_price, actual_price;
            try{
                var_price =  parseFloat($(this).attr('data-price'));
                actual_price =  parseFloat($(this).attr('actual-price'));

                // update current price
                var str_price = 'Rs. ' + var_price.toString() + '/-';
                $('#total-price').text(str_price);
                $('#total-price').attr("sum-price", var_price);

            
                var show_price = 'Rs. ' + actual_price.toString() + '/';
                $('#id-total-actual-price').text(show_price);
                $('#id-total-actual-price').attr("total-actual-price", actual_price);

                try{
                    var per_off;
                    per_off = actual_price - var_price;
                    per_off = (per_off/actual_price)*100
                    per_off = Math.round(per_off);
                    $('#id_percentage-off').attr("percentage-off", per_off);
                    var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
                    $('#id_percentage-off').text(str_off);

                }catch(err){
                    console.log(err);
                }

            }catch(err){
                console.log(err);
            }

        }
    });


    $('input[name="fbt"]').click(function(){
        if ($(this).is(':checked'))
        {
            var fbt_price, sum_price, actual_price, actual_total;
            try{
                fbt_price =  parseFloat($(this).attr('data-price'));
                actual_price = parseFloat($(this).attr('actual-price'));
                try{
                    sum_price = parseFloat($('#total-price').attr('sum-price'));
                    actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

                    // current price update
                    sum_price = fbt_price + sum_price;
                    var show_price = 'Rs. ' + sum_price.toString() + '/-';
                    $('#total-price').text(show_price);
                    $("#total-price").attr("sum-price", sum_price);

                    // actual price update
                    actual_total = actual_price + actual_total;
                    var show_price = 'Rs. ' + actual_total.toString() + '/';
                    $('#id-total-actual-price').text(show_price);
                    $("#id-total-actual-price").attr("total-actual-price", actual_total);

                    try{
                        var per_off;
                        per_off = actual_total - sum_price;
                        per_off = (per_off/actual_total)*100
                        per_off = Math.round(per_off);
                        $('#id_percentage-off').attr("percentage-off", per_off);
                        var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
                        $('#id_percentage-off').text(str_off);

                    }catch(err){
                        console.log(err);
                    }


                }catch(err){
                    console.log(err);
                }
                
            }catch(err){
                console.log(err);
            }
            
        }
        else{

            var fbt_price, sum_price, actual_price, actual_total;
            try{
                fbt_price =  parseFloat($(this).attr('data-price'));
                actual_price = parseFloat($(this).attr('actual-price'));
                try{
                    sum_price = parseFloat($('#total-price').attr('sum-price'));
                    actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

                    // current price update
                    sum_price = sum_price - fbt_price;
                    var show_price = 'Rs. ' + sum_price.toString() + '/-';
                    $('#total-price').text(show_price);
                    $("#total-price").attr("sum-price", sum_price);

                    // actual price update
                    actual_total = actual_total - actual_price;
                    var show_price = 'Rs. ' + actual_total.toString() + '/';
                    $('#id-total-actual-price').text(show_price);
                    $("#id-total-actual-price").attr("total-actual-price", actual_total);

                    try{
                        var per_off;
                        per_off = actual_total - sum_price;
                        per_off = (per_off/actual_total)*100
                        per_off = Math.round(per_off);
                        $('#id_percentage-off').attr("percentage-off", per_off);
                        var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
                        $('#id_percentage-off').text(str_off);

                    }catch(err){
                        console.log(err);
                    }


                }catch(err){
                    console.log(err);
                }
                
            }catch(err){
                console.log(err);
            }

        }
    });

    $('input[name="required_option"]').click(function(){
        if ($(this).is(':checked'))
        {
            var req_price, sum_price, actual_price, actual_total;
            try{
                req_price =  parseFloat($(this).attr('data-price'));
                actual_price = parseFloat($(this).attr('actual-price'));
                try{
                    sum_price = parseFloat($('#total-price').attr('sum-price'));
                    actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

                    // current price updation
                    sum_price = req_price + sum_price;
                    var show_price = 'Rs. ' + sum_price.toString() + '/-';
                    $('#total-price').text(show_price);
                    $("#total-price").attr("sum-price", sum_price);

                    // actual price updation
                    actual_total = actual_total + actual_price;
                    var show_price = 'Rs. ' + actual_total.toString() + '/';
                    $('#id-total-actual-price').text(show_price);
                    $("#id-total-actual-price").attr("total-actual-price", actual_total);

                    // update percentage-off
                    try{
                        var per_off;
                        per_off = actual_total - sum_price;
                        per_off = (per_off/actual_total)*100
                        per_off = Math.round(per_off);
                        $('#id_percentage-off').attr("percentage-off", per_off);
                        var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
                        $('#id_percentage-off').text(str_off);

                    }catch(err){
                        console.log(err);
                    }

                }catch(err){
                    console.log(err);
                }

            }catch(err){
                console.log(err);
            }
            
        }
        else{

            var req_price, sum_price, actual_price, actual_total;
            try{
                req_price =  parseFloat($(this).attr('data-price'));
                actual_price = parseFloat($(this).attr('actual-price'));
                try{
                    sum_price = parseFloat($('#total-price').attr('sum-price'));
                    actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

                    // current price updation
                    sum_price = sum_price - req_price;
                    var show_price = 'Rs. ' + sum_price.toString() + '/-';
                    $('#total-price').text(show_price);
                    $("#total-price").attr("sum-price", sum_price);

                    // actual price updation
                    actual_total = actual_total - actual_price;
                    var show_price = 'Rs. ' + actual_total.toString() + '/';
                    $('#id-total-actual-price').text(show_price);
                    $("#id-total-actual-price").attr("total-actual-price", actual_total);

                    // update percentage-off
                    try{
                        var per_off;
                        per_off = actual_total - sum_price;
                        per_off = (per_off/actual_total)*100
                        per_off = Math.round(per_off);
                        $('#id_percentage-off').attr("percentage-off", per_off);
                        var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
                        $('#id_percentage-off').text(str_off);

                    }catch(err){
                        console.log(err);
                    }

                }catch(err){
                    console.log(err);
                }

            }catch(err){
                console.log(err);
            }

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
                        var info = 'Added to cart. You have '+ json.cart_count + ' products in cart.'
                        $('#id-cart-message').text(info);
                        // alert("product added in cart successfully");
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
