$(function(){
	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();
        console.log(action_type);
		if (action_type == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_welcome').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if ( selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected ' + selected.length + ' orders to do action' + ' ?</div>');
                $('#action_welcome').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select order id first.</div>');
	            $('#action_welcome').hide();
	            $('#actionModal').modal("show");

            }
            
        }

	});


	$('#action_welcome').click(function(){
        var action = $('#id_action').val();

        $('#action_type_id').val(action);

        
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_welcome').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if (selected.length > 0){
            	$("#welcome_table_form").submit();
            	$('#actionModal').modal("hide");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orders id, Please select orders first.</div>');
	            $('#action_welcome').hide();
	            $('#actionModal').modal("show");
            } 
        }
    });


    $(document).on('change', '#id-cat', function(){
        var select = $('#id-subcat');
        select.empty();
        select.append("<option value=''>Select SubCategory</option>");
        replaced_order_items = 0
        var parent = $(this).val();

        if (parent == '21'){
            $("#id-message").prop('required', false);
        }
        else{
            $("#id-message").prop('required', true);
        }


        switch(parent){ 
            case '21':{
                $("#sub_cat1 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }
            case '22':{
                $("#sub_cat2 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }
            case '23':{
                $("#sub_cat3 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }  
            default: //default child option is blank
                break;
            }
    });

    $(document).on('change', '#id-subcat', function(){
        var parent = $(this).val(); 
        var parent_this = $(this);
        switch(parent){ 
            case '41':{
                $(".sub_cat_item").each(function() {
                    if($(this).is(':enabled')) {
                        var select = $(this);
                        select.empty();
                        select.append("<option value="+ parent_this.val() + ">" + parent_this.find('option:selected').text() + "</option>");
                    }
                });
                
                break;
            }

            case '42':{
                $(".sub_cat_item").each(function() {
                    var select = $(this);
                    select.empty();
                    select.append("<option value="+ parent_this.val() + ">" + parent_this.find('option:selected').text() + "</option>");
                    
                });
                
                break;
            }

            case '61':{
                $(".sub_cat_item").each(function() {
                    var select = $(this);
                    select.empty();
                    select.append("<option value=''>Select SubCategory</option>");
                    $("#sub_cat_service option").each(function(){
                        select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                    });
                });
                break;
            }
            case '81':{
                $(".sub_cat_item").each(function() {
                    var select = $(this);
                    select.empty();
                    select.append("<option value="+ parent_this.val()+ ">" + parent_this.find('option:selected').text() + "</option>");
                });
                break;
            } 
            case '82':{
                $(".sub_cat_item").each(function() {
                    var select = $(this);
                    select.empty();
                    select.append("<option value="+ parent_this.val()+ ">" + parent_this.find('option:selected').text() + "</option>");
                });
                break;
            }
            case '83':{
                $(".sub_cat_item").each(function() {
                    var select = $(this);
                    select.empty();
                    select.append("<option value="+ parent_this.val()+ ">" + parent_this.find('option:selected').text() + "</option>");
                });
                break;
            } 
            default: //default child option is blank
                break;
        }
        
    });

    $(document).on("change", "#id-welcome-call-form", function() {
        var cat = $("#id-cat").val();
        var $followdiv = $("#id-follow-div");
        var $follow = $("#id-follow")
        if(cat == "23")
        {
            $followdiv.show();
            $follow.attr('required', true);
        }
        else{
            $followdiv.hide();
            $follow.attr('required', false);
        }
    });

    $(document).on("change", ".sub_cat_item", function() {

        var sub_cat_value = $(this).val();
        if(sub_cat_value == 65) {
            temp_id = $(this).attr('data-target')
            $("#"+temp_id).css("display","")
        }
        else{
            temp_id = $(this).attr('data-target')
            $("#"+temp_id).css("display","none")
        }
    });

    $(document).on("click", "#id-welcomecall-update", function() {
        $('#id-welcome-call-form').parsley().validate();
        if($('#id-welcome-call-form').parsley().isValid()){
            $('#id-welcome-call-form').submit();
        }
    });

    var d = new Date($.now());
    $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd hh:ii:ss",
        autoclose: true,
        todayBtn: true,
        minuteStep: 5,
        startDate: d
    });

});
