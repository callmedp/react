
   function getProductDetail(vendor_id,category_id){
   $.ajax({
               url: '/api/v1/get-products/',
               type: "GET",
               data : {'type_flow': 16, 'category' : category_id, 'vendor':vendor_id ,'fl':'id,inr_price,name,heading,absolute_url,num_jobs'},
               dataType: 'json',
               success: function(json) {
                if(json.count >=1 ){
                    prod_id =json.results[0].id;
                    $('#test-price').text('');
                    $('#test-product-name').text('');
                    $('#test-product-name').text(json.results[0].name);
                    $('#test-product-name').attr('href',json.results[0].absolute_url)
                    $('#viewPaidTest').attr('href',json.results[0].absolute_url)
                    $('#test-price').text("Rs. " + json.results[0].inr_price);
                    $('#test-product').removeAttr('style');
                }
                else{
                     $('#test-price').text('');
                    $('#test-product-name').text('');
                    $('#test-price').text("");
                   $('#test-product-name').attr('href',"#");
                }
               },
               error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again");

               }
           });


   }


   function addToCart(vendor_id,category_id){
   $.ajax({
               url: '/api/v1/get-products/',
               type: "GET",
               data : {'type_flow': 16, 'category' : category_id, 'vendor':vendor_id},
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

   function getCourseDetail(vendor_id,category_id,test_id){
   $.ajax({
               url: '/api/v1/get-products/',
               type: "GET",
               data : {'type_flow': 2, 'category' : category_id, 'vendor':vendor_id },
               dataType: 'json',
               success: function(json) {
                if(json.count >=1 ){
                console.log(json.results[0].absolute_url);
                $('#courseName').text(json.results[0].title);
                $('#coursePrice').text(json.results[0].inr_price);
                $('#courseDuration').text(json.results[0].day_duration);
                $('#courseName').attr('href',json.results[0].absolute_url)
                $('#courseImg').attr('src',json.results[0].image)
                $('#courseJobsAvailable').text(json.results[0].num_jobs);
                $('#courseCartBtn').click(function(){
                updateToCart(json.results[0].id,'cart');
                });
                $('#testCourse').removeAttr('style');

                }
               },
               error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, Please try again");

               }
           });


   }

   function testSession(data){
        $.ajax({
         url   : '/api/v1/set-session/',
         data: data,
         type  : 'post',
         success: function(response){
            return false;
         }
    });

}