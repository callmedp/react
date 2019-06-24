
   function getProductDetail(vendor_id,category_id){
   $.ajax({
               url: '/api/v1/get-products/',
               type: "GET",
               data : {'type_flow': 16, 'category' : category_id, 'vendor':vendor_id ,'fl':'id,inr_price'},
               dataType: 'json',
               success: function(json) {
                if(json.count >=1 ){
                    prod_id =json.results[0].id;
                    $('#'+ category_id + '-price').text('');
                    $('#'+ category_id+  '-price').text("Rs. " + json.results[0].inr_price);
                }
               },
               error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again");

               }
           });
           debugger;

   }


   function addToCart(vendor_id,category_id){
   $.ajax({
               url: '/api/v1/get-products/',
               type: "GET",
               data : {'type_flow': 16, 'category' : 3, 'vendor':1},
               dataType: 'json',
               success: function(json) {
                if(json.count >=1 ){
                    prod_id =json.results[0].id;
                    cart_type = 'cart';
                    updateToCart(prod_id,cart_type);

                }
               },
               error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again");

               }
           });

   }

   function updateToCart(prod_id,cart_type)
   {
   $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: { 'prod_id': prod_id,'cart_type': cart_type,},
                dataType: 'json',
                success: function(json) {
                    if (json.status == 1){

                        window.location.href = json.cart_url
                    }
                    else if (json.status == -1){
                        alert("Something went wrong, Please try again.");
                    }

                },
                failure: function(response){
                    alert("Something went wrong, Please try again");

                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong, Please try again");
                }
            });
        }
