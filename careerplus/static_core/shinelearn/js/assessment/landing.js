       $('#testModal').on('show.bs.modal', function(e) {
        var modalobject = JSON.parse(e.relatedTarget.dataset.attrValue);
        $('#productName').text(modalobject.productName);
        $('#productDuration').text(modalobject.productDuration);
        $('#productPrice').text(modalobject.productPrice);
        $('#courseDuration').text(modalobject.courseDuration);
        $('#coursePrice').text(modalobject.coursePrice);
        $('#courseName').text(modalobject.courseName);
        $('#questCount').text(modalobject.quescount);
        if(modalobject.courseName == ""|| modalobject.courseName == "undefined" ){
        $('#testCourse').hide();
        }
        else{
         $('#testCourse').show();
        }
        $('#startTestLink').attr("href",'/practice-tests/'+ modalobject.testSlug +'-test/');
        $('#testAddToCart').click( function()
         {
            updateToCart(modalobject.productId,'cart');
         }
      );
        $('#courseCartBtn').click(function(){
        updateToCart(modalobject.courseId,'cart');
        });
});


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

   function updateToCart(prod_id,cart_type='cart')
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
