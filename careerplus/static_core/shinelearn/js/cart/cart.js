
function removeFromCart(line_id){
    if (line_id){
        
        $('#id-remove-cart' + line_id).addClass('disabled').removeAttr("onclick");
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

function deliveryOptionUpdate(line_id){
    if (line_id){
        var formData = $('#delivery-option-form' + line_id).serialize();
        $.ajax({
            url: '/cart/update-deliverytype/',
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function(data, textStatus, jqXHR){
                if (data.total_cart_amount != -1 && data.delivery_charge != -1){
                    if (data.delivery_charge){
                        var text_str = '+ Rs. ' + data.delivery_charge.toString() + '/-';
                        $('#delivery-charge' + line_id).text(text_str);
                    }
                    else{
                        $('#delivery-charge' + line_id).text('');
                    }
                    $('#total-cart-amount-id').html(
 '<strong>Rs.' +  data.total_cart_amount + ' /-<small style="font-size:12px; font-weight:normal; color:#999; margin-left:5px">+(taxes)</small></strong>');
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

function update_variation_price(req_price, actual_price){
    var req_price = req_price, actual_price = actual_price, sum_price, actual_total
    try{
        sum_price = parseFloat($('#total-price').attr('sum-price'));
        console.log(sum_price);
        actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));
        // current price updation
        sum_price = req_price + sum_price;
        var show_price = 'Rs. ' + sum_price.toString() + '/- ' + '<small>(+taxes)</small>';

        var scroll_price = 'Rs. ' + sum_price.toString() + '/-';
        $('#id-scroll-price').html(scroll_price);
        $("#id-scroll-price").attr("sum-price", sum_price);

        $('#total-price').html(show_price);
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
}

function updateCheckedPrice(this_obj){
            
    var fbt_price, sum_price, actual_price, actual_total;
    try{
        fbt_price =  parseFloat($(this_obj).attr('data-price'));

        //actual_price = parseFloat($(this_obj).attr('actual-price'));
        
        if(typeof $(this).attr('actual-price') != "undefined"){
            actual_price =  parseFloat($(this).attr('actual-price'));
        } else{
            actual_price =  parseFloat($(this).data('actual-price'));
        }

        try{
            sum_price = parseFloat($('#total-price').attr('sum-price'));
            actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

            // current price update
            sum_price = fbt_price + sum_price;
            var show_price = 'Rs. ' + sum_price.toString() + '/- ' + '<small>(+taxes)</small>';

            var scroll_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#id-scroll-price').html(scroll_price);
            $("#id-scroll-price").attr("sum-price", sum_price);
            
            $('#total-price').html(show_price);
            $("#total-price").attr("sum-price", sum_price);

            // actual price update
            actual_total = actual_price + actual_total;

            if (actual_total > sum_price){
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
            }

        }catch(err){
            console.log(err);
        }
        
    }catch(err){
        console.log(err);
    }
}

function updateUnCheckedPrice(this_obj){
    
    var fbt_price, sum_price, actual_price, actual_total;
    try{
        fbt_price =  parseFloat($(this_obj).attr('data-price'));
        //actual_price = parseFloat($(this_obj).attr('actual-price'));
        if(typeof $(this).attr('actual-price') != "undefined"){
            actual_price =  parseFloat($(this).attr('actual-price'));
        } else{
            actual_price =  parseFloat($(this).data('actual-price'));
        }
        try{
            sum_price = parseFloat($('#total-price').attr('sum-price'));
            actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

            // current price update
            sum_price = sum_price - fbt_price;
            var show_price = 'Rs. ' + sum_price.toString() + '/- ' + '<small>(+taxes)</small>';

            var scroll_price = 'Rs. ' + sum_price.toString() + '/-';
            $('#id-scroll-price').html(scroll_price);
            $("#id-scroll-price").attr("sum-price", sum_price);

            $('#total-price').html(show_price);
            $("#total-price").attr("sum-price", sum_price);

            // actual price update
            actual_total = actual_total - actual_price;

            if (actual_total > sum_price){
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
            }


        }catch(err){
            console.log(err);
        }
        
    }catch(err){
        console.log(err);
    }
}

function toggler(divId) {
    $("#" + divId).toggle();
}

function updateCartPrice(){

    $('input[name="radio"]').each(function(){
        if ($(this).is(':checked')){
            var var_price, actual_price;
            try{
                var_price =  parseFloat($(this).attr('data-price'));
                if(typeof $(this).attr('actual-price') != "undefined"){
                    actual_price =  parseFloat($(this).attr('actual-price'));
                } else{
                    actual_price =  parseFloat($(this).data('actual-price'));
                }

                // update current price
                var str_price = 'Rs. ' + var_price.toString() + '/- ' + '<small>(+taxes)</small>';

                var scroll_price = 'Rs. ' + var_price.toString() + '/-';
                $('#id-scroll-price').html(scroll_price);
                $("#id-scroll-price").attr("sum-price", var_price);

                $('#total-price').html(str_price);
                $('#total-price').attr("sum-price", var_price);

                if (actual_price > var_price){
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
                }

            }catch(err){
                console.log(err);
            }
        }
    });

    $('input[name="required_option"]').each(function(){
        if ($(this).is(':checked')){
            updateCheckedPrice(this);
        }
    });

    $('input[name="fbt"]').each(function(){
        if ($(this).is(':checked')){
            updateCheckedPrice(this);
        }
    });

}

function checkedInitialRequired(){
    var req_selected = true;
    $('input[name="required_option"]').each(function(){
        if ($(this).is(':checked')){
            req_selected = false;
            return false;
        }
    });

    if (req_selected){
        $('input[name="required_option"]').each(function(){
            if (!$(this).is(':checked')){
                try{
                    // req_price =  parseFloat($(this).attr('data-price'));
                    // actual_price = parseFloat($(this).attr('actual-price'));
                    // update_variation_price(req_price, actual_price);
                    $(this).attr('checked', true);
                    // console.log(req_price, actual_price);

                }catch(err){
                    console.log(err);
                }
            }
            return false;
        });
    }
}

function cartScroller() {
  var item = $('.price-box'),
  height = item.height();
  $(window).scroll(function(){
      var $recommendProductDiv = $('.recomend-product-bg');
      if ($recommendProductDiv.length && item.length) {
          if (item.offset().top + height > $recommendProductDiv.offset().top - 50) {
              item.css({'visibility': 'hidden'})
          } else {
              item.css({'visibility': 'visible'});
          }
      }
  });
}

$(document).ready(function(){

    checkedInitialRequired();  // for country specific products
    updateCartPrice();

    $(document).on( "click", 'input[name="radio"]', function(e){
        if ($(this).is(':checked'))
        {
            var var_price, actual_price;
            try{
                var_price =  parseFloat($(this).attr('data-price'));
                if(typeof $(this).attr('actual-price') != "undefined"){
                    actual_price =  parseFloat($(this).attr('actual-price'));
                } else{
                    actual_price =  parseFloat($(this).data('actual-price'));
                }

                // update current price
                var str_price = 'Rs. ' + var_price.toString() + '/- ' + '<small>(+taxes)</small>';

                var scroll_price = 'Rs. ' + var_price.toString() + '/-';
                $('#id-scroll-price').html(scroll_price);
                $("#id-scroll-price").attr("sum-price", var_price);

                $('#total-price').html(str_price);
                $('#total-price').attr("sum-price", var_price);

                if (actual_price > var_price){
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
                }

            }catch(err){
                console.log(err);
            }

        }
    });


    $(document).on( "click", 'input[name="fbt"]', function(e){
        if ($(this).is(':checked'))
        {
            updateCheckedPrice(this);
            /*var fbt_price, sum_price, actual_price, actual_total;
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
            }*/
            
        }
        else{

            updateUnCheckedPrice(this);

            // var fbt_price, sum_price, actual_price, actual_total;
            // try{
            //     fbt_price =  parseFloat($(this).attr('data-price'));
            //     actual_price = parseFloat($(this).attr('actual-price'));
            //     try{
            //         sum_price = parseFloat($('#total-price').attr('sum-price'));
            //         actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

            //         // current price update
            //         sum_price = sum_price - fbt_price;
            //         var show_price = 'Rs. ' + sum_price.toString() + '/-';
            //         $('#total-price').text(show_price);
            //         $("#total-price").attr("sum-price", sum_price);

            //         // actual price update
            //         actual_total = actual_total - actual_price;
            //         var show_price = 'Rs. ' + actual_total.toString() + '/';
            //         $('#id-total-actual-price').text(show_price);
            //         $("#id-total-actual-price").attr("total-actual-price", actual_total);

            //         try{
            //             var per_off;
            //             per_off = actual_total - sum_price;
            //             per_off = (per_off/actual_total)*100
            //             per_off = Math.round(per_off);
            //             $('#id_percentage-off').attr("percentage-off", per_off);
            //             var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
            //             $('#id_percentage-off').text(str_off);

            //         }catch(err){
            //             console.log(err);
            //         }


            //     }catch(err){
            //         console.log(err);
            //     }
                
            // }catch(err){
            //     console.log(err);
            // }

        }
    });

    $(document).on( "click", 'input[name="required_option"]', function(e){
        if ($(this).is(':checked'))
        {
            updateCheckedPrice(this);
            // var req_price, sum_price, actual_price, actual_total;
            // try{
            //     req_price =  parseFloat($(this).attr('data-price'));
            //     actual_price = parseFloat($(this).attr('actual-price'));
            //     update_variation_price(req_price, actual_price);
            //     // try{
            //     //     sum_price = parseFloat($('#total-price').attr('sum-price'));
            //     //     actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

            //     //     // current price updation
            //     //     sum_price = req_price + sum_price;
            //     //     var show_price = 'Rs. ' + sum_price.toString() + '/-';
            //     //     $('#total-price').text(show_price);
            //     //     $("#total-price").attr("sum-price", sum_price);

            //     //     // actual price updation
            //     //     actual_total = actual_total + actual_price;
            //     //     var show_price = 'Rs. ' + actual_total.toString() + '/';
            //     //     $('#id-total-actual-price').text(show_price);
            //     //     $("#id-total-actual-price").attr("total-actual-price", actual_total);

            //     //     // update percentage-off
            //     //     try{
            //     //         var per_off;
            //     //         per_off = actual_total - sum_price;
            //     //         per_off = (per_off/actual_total)*100
            //     //         per_off = Math.round(per_off);
            //     //         $('#id_percentage-off').attr("percentage-off", per_off);
            //     //         var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
            //     //         $('#id_percentage-off').text(str_off);

            //     //     }catch(err){
            //     //         console.log(err);
            //     //     }

            //     // }catch(err){
            //     //     console.log(err);
            //     // }

            // }catch(err){
            //     console.log(err);
            // }
            
        }
        else{

            updateUnCheckedPrice(this);

            // var req_price, sum_price, actual_price, actual_total;
            // try{
            //     req_price =  parseFloat($(this).attr('data-price'));
            //     actual_price = parseFloat($(this).attr('actual-price'));
            //     try{
            //         sum_price = parseFloat($('#total-price').attr('sum-price'));
            //         actual_total = parseFloat($('#id-total-actual-price').attr('total-actual-price'));

            //         // current price updation
            //         sum_price = sum_price - req_price;
            //         var show_price = 'Rs. ' + sum_price.toString() + '/-';
            //         $('#total-price').text(show_price);
            //         $("#total-price").attr("sum-price", sum_price);

            //         // actual price updation
            //         actual_total = actual_total - actual_price;
            //         var show_price = 'Rs. ' + actual_total.toString() + '/';
            //         $('#id-total-actual-price').text(show_price);
            //         $("#id-total-actual-price").attr("total-actual-price", actual_total);

            //         // update percentage-off
            //         try{
            //             var per_off;
            //             per_off = actual_total - sum_price;
            //             per_off = (per_off/actual_total)*100
            //             per_off = Math.round(per_off);
            //             $('#id_percentage-off').attr("percentage-off", per_off);
            //             var str_off = ' ' + per_off.toString() + '%' + ' ' + 'off';
            //             $('#id_percentage-off').text(str_off);

            //         }catch(err){
            //             console.log(err);
            //         }

            //     }catch(err){
            //         console.log(err);
            //     }

            // }catch(err){
            //     console.log(err);
            // }

        }
    });


    $(document).on( "click", "#add-to-cart", function(e){
        ga('send', 'event', 'Buy Flow', 'Enroll Now');
        e.preventDefault();
        $('#add-to-cart').attr('disabled', true);

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
                        console.log('----here', json);
                        var info = 'Added to cart. You have '+ json.cart_count + ' products in cart.'
                        // $('#id-cart-message').text(info);
                        $('#cart-counter-id').addClass('cart-counter');
                        $('#cart-counter-id').text(json.cart_count);
                        // if (window.CURRENT_FLAVOUR == 'mobile'){
                        //     alert("Product added successfully in cart.");
                        // }
                        window.location.href = json.cart_url
                    }
                    else if (json.status == -1){
                        alert("Something went wrong, Please try again.");
                    }
                    $('#add-to-cart').attr('disabled', false);

                },
                failure: function(response){
                    alert("Something went wrong, Please try again");
                    $('#add-to-cart').attr('disabled', false);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong, Please try again");
                    $('#add-to-cart').attr('disabled', false);
                }
            });
        }

    });


    $(document).on( "click", "#enrol-now-button", function(e){
        e.preventDefault();
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

    cartScroller();
       $('.js-check').each(function(){
            if($(this).is(':checked')){
                $(this).closest('.parent-check').addClass('selected');
            }
            else{
                $(this).closest('.parent-check').removeClass('selected');   
            }
            }); 
    
    $(document).on('change', '.js-check', function() {
        if($(this).is(':checked')){
            $(this).closest('.parent-check').addClass('selected');

        }
        else{
            $(this).closest('.parent-check').removeClass('selected');   
        }
    });



});
