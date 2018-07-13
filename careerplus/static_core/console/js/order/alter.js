
function alt_email_update(email_id,order_id)
{
document.getElementById('alter_email').value=email_id ;
document.getElementById("order_id").value=order_id ;
$("#emailmodal").modal();
}

function alt_num_update(alt_num,order_id)
{
document.getElementById('alt_num').value=alt_num ;
document.getElementById('order_id1').value=order_id;
$("#numbermodal").modal();
}


function email_alt_update(){

        var formData = $('#alteremail').serialize();
        console.log('hello-0-0-----',formData)
        $.ajax({
            url: '/ajax/order/orderlistmodal/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 'success'){
	            	alert('successfully updated');
	            	window.location.reload();
            	}
            	else{
            		alert("Unsuccessful");
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
};

function numb_alt_update(){

        var formData = $('#alternumber').serialize();
        console.log('hello-0-0-----',formData)
        $.ajax({
            url: '/ajax/order/orderlistmodal/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 'success'){
	            	alert('successfully updated');
	            	window.location.reload();
            	}
            	else{
            		alert("Unsuccessful");
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
};


