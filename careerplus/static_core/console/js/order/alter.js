var emailtemp;
var mobitemp;
function alt_email_update(email_id,order_id)
{
document.getElementById('primary_email').innerHTML=email_id ;
document.getElementById("order_id").value=order_id ;
document.getElementById("email-error").innerHTML='';
$('#alteremail').parsley().reset();
$('#alteremail')[0].reset();

$("#emailmodal").modal();
}

function alt_num_update(alt_num,order_id)
{
document.getElementById('primary_mobile').value=alt_num ;
document.getElementById('order_id1').value=order_id;
document.getElementById("mobile-error").innerHTML='';
$('#alternumber').parsley().reset();
$('#alternumber')[0].reset();

$("#numbermodal").modal();
}

function email_alt_update(){
        var formData = $('#alteremail').serialize();
        var form = $('#alteremail');
        form.parsley().validate();
         if (form.parsley().isValid()){
        $.ajax({
            url: '/ajax/order/orderlistmodal/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 'success'){
	            	alert('successfully updated');
	            	if (json.obj_altemail){
	            	    document.getElementById(json.object_id).innerHTML='<span><b>Alt</b>-'+json.obj_altemail + "</span>";
                }
                $("#emailmodal").modal('hide');

           	}
            	else{
            		document.getElementById("email-error").innerHTML='<div class="alert alert-danger"><strong>'+json.error +'</strong></div>';
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
        }
};

function numb_alt_update(){

        var formData = $('#alternumber').serialize();
        var form = $('#alternumber');
        form.parsley().validate();
         if (form.parsley().isValid()){
        $.ajax({
            url: '/ajax/order/orderlistmodal/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 'success'){
	            	alert('successfully updated');
	            	document.getElementById(json.object_id).innerHTML = ' <span><b>Alt</b>-'+json.obj_altnum+"</span>";
                    $("#numbermodal").modal('hide');
           	}
            	else{
            	document.getElementById("mobile-error").innerHTML='<div class="alert alert-danger"><strong>'+json.error +'</strong></div>';

            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }

        });
        }
};

//
$('#alteremail').submit(function(event){
 event.preventDefault();

 email_alt_update();
});

$('#alternumber').submit(function(event){
 event.preventDefault();
 numb_alt_update();

});

//$('#alteremail').validate({
//  rules: {
//    alt_email: {
//      required: true,
//      email: true
//    }
//  }
//});
