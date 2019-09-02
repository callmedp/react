$(document).ready(function() {

    $('.enrol-now-button').click(function() {
        var prod_id = $('.enrol-now-button').attr('prod-id');
        ga('send', 'event', 'Buy Flow', 'Enroll Now',prod_id);
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

            console.log(prod_id);

            data = {
                "prod_id": prod_id,
                "addons": fbt,
                "cart_type": cart_type,
                "cv_id": cv_id,
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