let current_oi = null, selected_order_items = []

$(function(){

	$('#action_button_go').click(function(){
		var action = $('#id_action').val();
		if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_button').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' orderitems to do action' + ' ?</div>');
                $('#action_button').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select orderitems first to do actions.</div>');
	            $('#action_button').hide();
	            $('#actionModal').modal("show");
            }
            
        }

	});


	$('#action_button').click(function(){
        var action = $('#id_action').val();
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_button').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = [];
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
            	$('#actionModal').modal("hide");
                $('#selected-id').val(JSON.stringify(selected));
                $('#action_form').submit();
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
	            $('#action_button').hide();
	            $('#actionModal').modal("show");
            } 
        }
      
    });


    $('#assignment_button_go').click(function(){
        var action = $('#id_assign_to').val();
        if (action == 0){
            $('#assignmentModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#assignment_action_yes').hide();
            $('#assignmentModal').modal("show");
        }
        else{
            var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#assignmentModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' orderitems to assign' + ' ?</div>');
                $('#assignment_action_yes').show();
                $('#assignmentModal').modal("show");
            }
            else{
                $('#assignmentModalbody').html('<div class="alert alert-danger">Please select orderitems first to do actions.</div>');
                $('#assignment_action_yes').hide();
                $('#assignmentModal').modal("show");
            }
            
        }

    });


    $('#assignment_action_yes').click(function(){
        var action = $('#id_assign_to').val();
        if (action == 0){
            $('#assignmentModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#assignment_action_yes').hide();
            $('#assignmentModal').modal("show");
        }
        else{
            var selected = [];
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#assignmentModalbody').modal("hide");
                $('#selected-id-assign').val(JSON.stringify(selected));
                $('#assignment_form').submit();
            }
            else{
                $('#assignmentModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
                $('#assignment_action_yes').hide();
                $('#assignmentModal').modal("show");
            } 
        }
      
    });

});


function redirectToShineProfile(oi_id){
    if (oi_id){
        var formData = $('#redirecShineForm' + oi_id).serialize();
        $.ajax({
            url: '/ajax/autologin/tokengenerator/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(data){
                if (data.status){
                    var token = data.token;
                    var link = window.SHINE_SITE + '/myshine/login/' + token + '/'
                    window.open(link, '_blank');
                    // window.open(link, 'width=650,height=450,scrollbars=yes');
                }
                else{
                    var msg = data.display_message;
                    alert(msg);
                }
                // window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};

const getOrderItems = (order_id)=>{
    $('.loader-div').show()
    $('body').addClass('body-overflow')
    selected_order_items =[]
    current_oi = order_id
    $.get(`/order/api/v1/order/${current_oi}/items`,(data)=>{
        $('#order-items').empty()
        if(data['count']){
            for(let oi of data['results']){
                
                $('#order-items').append(
                    `
                        <div>
                            <input type="checkbox" checked onclick="updateSelectedOI(this,${oi.id})" value="${oi.id}">${oi.product_name}
                        </div>
                    `
                )
                selected_order_items.push(oi.id)
            }   
            $('#oi_item_error').hide()
            $('#upload-doc-modal').modal('show')
            $('.loader-div').hide()
            $('body').removeClass('body-overflow')
        }
        
        
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'OrderItems not loaded'
        })
    })
}

$(document).ready(function(){
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });
    
    
})

const updateSelectedOI = (checkbox,oi_id)=>{
    $('#oi_item_error').hide()
    if(checkbox.checked){
        selected_order_items.push(oi_id)
    }
    else{
        let index = selected_order_items.indexOf(oi_id)
        if (index !== -1) selected_order_items.splice(index, 1);  
    }
    if(!selected_order_items.length){
        $('#oi_item_error').show()
    }
}

const upload_click = ()=>{
    if(!selected_order_items.length)
        return
    $('#oi_ids').attr("value",()=>{return selected_order_items.join(" ")})
    $("#resume-upload-form").submit();
    $('#upload-doc-modal').modal('hide')
 }
