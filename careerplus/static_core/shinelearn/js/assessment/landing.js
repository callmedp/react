$('#testModal').on('show.bs.modal', function (e) {
    var modalobject = JSON.parse(e.relatedTarget.dataset.attrValue);
    $('#productName').text(modalobject.productName);
    $('#productName').attr("href", modalobject.productUrl);
    $('#productName').attr("title", modalobject.productName);
    $('#productDuration').text(modalobject.productDuration);
    $('#productPrice').text('Rs. ' + Math.floor(parseInt(modalobject.productPrice)));
    $('#courseDuration').text(modalobject.courseDuration);
    $('#coursePrice').text('Rs. ' + modalobject.coursePrice);
    $('#courseName').text(modalobject.courseName);
    $('#courseName').attr("href", modalobject.courseUrl);
    $('#courseName').attr("title", modalobject.courseName);
    $('#questCount').text(modalobject.quescount);
    $('#exampleModalLongTitle').text(modalobject.catname);
    $('#fakeCoursePrice').text('Rs. ' + parseInt(parseInt(modalobject.coursePrice) / 0.9));
    $('#fakeProductPrice').text('Rs. ' + parseInt(parseInt(modalobject.productPrice) / 0.9));
    

    console.log('marg', modalobject.redeem_test);

    if (modalobject.redeem_test == "True") {
        $('#price_box_vskill').addClass('flex-column');
    }
    if (modalobject.courseName == "" || modalobject.courseName == "undefined") {
        $('#testCourse').hide();
    }
    if (modalobject.redeem_count != '0') {

        $('[data-toggle="tooltip"]').tooltip({
            title: `You have ${modalobject.redeem_count} free practice test (Assessment) as you're a Shine Premium User`,
            placement: "top"
        })

    }

    else {
        $('#testCourse').show();
    }
    $('#startTestLink').attr("href", '/practice-tests/' + modalobject.testSlug + '-test/');
    $('#testAddToCart').click(function () {
        ga('send', 'event', 'Buy Flow', 'Enroll Now', modalobject.productId);
        updateToCart(modalobject.productId, 'cart');
    }
    );
    $('#courseCartBtn').click(function () {
        courseUpdateToCart(modalobject.courseId, 'cart');
    });

    //  create direct order on Redeeming the Test and Update the ProductPoint Record
    $('#createOrderForTest').click(function () {
        $('#testModal').modal('hide')
        $('.overlay-background').show()
        $('body').addClass('body-noscroll')
        createDirectOrder(modalobject.productId, modalobject.redeem_option)
    })
});


function testSession(data) {
    $.ajax({
        url: '/api/v1/set-session/',
        data: data,
        type: 'post',
        success: function (response) {

            return false;
        }
    });

}


function courseUpdateToCart(prod_id, cart_type = 'cart') {
    $.ajax({
        url: '/cart/add-to-cart/',
        type: 'POST',
        data: { 'prod_id': prod_id, 'cv_id': prod_id, 'cart_type': cart_type, },
        dataType: 'json',
        success: function (json) {
            if (json.status == 1) {

                window.location.href = json.cart_url;

            }
            else if (json.status == -1) {
                alert("Something went wrong, Please try again.");
            }

        },
        failure: function (response) {
            alert("Something went wrong, Please try again");

        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Something went wrong, Please try again");
        }
    });
}

function createDirectOrder(productId, redeem_option) {

    $.ajax({
        url: '/api/v1/order/direct-order/',
        type: 'POST',
        data: { 'prod_id': productId, 'redeem_option': redeem_option },
        dataType: 'json',
        success: function (json) {
            if (json.status == 1) {
                window.location.href = json.redirectUrl;
            }
            else if (json.status == -1) {
                $('.overlay-background').hide()
                $('body').removeClass('body-noscroll')
                alert(json.error_message);
            }

        },
        failure: function (response) {
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')
            alert("Something went wrong, Please try again");

        },
        error: function (xhr, ajaxOptions, thrownError) {
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')
            alert("Something went wrong, Please try again");
        }
    });

}



function updateToCart(prod_id, cart_type = 'cart') {
    $.ajax({
        url: '/cart/add-to-cart/',
        type: 'POST',
        data: { 'prod_id': prod_id, 'cart_type': cart_type, },
        dataType: 'json',
        success: function (json) {
            if (json.status == 1) {

                window.location.href = json.cart_url;

            }
            else if (json.status == -1) {
                alert("Something went wrong, Please try again.");
            }

        },
        failure: function (response) {
            alert("Something went wrong, Please try again");

        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Something went wrong, Please try again");
        }
    });
}


function counter(facolor) {

    return facolor % 9;

}