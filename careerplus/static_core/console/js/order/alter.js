var emailtemp;
var mobitemp;
function alt_email_update(email_id,order_id)
{
console.log("ia m in altemail call")
emailtemp=email_id;
document.getElementById('id_alt_email').value=email_id ;
document.getElementById("order_id").value=order_id ;
document.getElementById("email-error").innerHTML='';
$('#alteremail').parsley().reset();
$("#emailmodal").modal();
}

function alt_num_update(alt_num,order_id)
{
mobitemp=alt_num;
document.getElementById('id_alt_mobile').value=alt_num ;
document.getElementById('order_id1').value=order_id;
document.getElementById("email-error").innerHTML='';
$('#alternumber').parsley().reset();
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
	            	    document.getElementById(json.object_id).innerHTML=emailtemp+'<br/><b>Alt</b>-'+json.obj_altemail;
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
	            	document.getElementById(json.object_id).innerHTML= json.country+ "-" + mobitemp + '<br/><span><b>Alt</b>-'+json.obj_altnum+"</span>";
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
 console.log("i am in alter")

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
