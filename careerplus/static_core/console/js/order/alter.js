var emailtemp;
var mobitemp;
function alt_email_update(order_id)
{
document.getElementById("order_id").value=order_id ;
document.getElementById("email-error").innerHTML='';
$('#alteremail').parsley().reset();
$('#alteremail')[0].reset();

$("#emailmodal").modal();
}

function alt_num_update(order_id)
{
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
	            	    document.getElementById('email'+json.object_id).innerHTML='<span id="email_field'+json.object_id+'"><b>Alt</b>- '+json.obj_altemail + "</span>";
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
	            	document.getElementById('mobile'+json.object_id).innerHTML = ' <span id="mobile_field'+json.object_id+'"><b>Alt</b>-'+json.obj_altnum+"</span>";
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

function createDraftResumeDownload(element){

if(element.oi_resume){
let oi_resume = element.oi_resume.split('/').pop()
return ` <div class="allactions__box"><strong>Candidate Resume:</strong></br>
         <a href="/console/queue/resumedownload/?path=${oi_resume}&next=${window.location.pathname}">
         <button type="button" class="btn btn-success btn-xs"><i class="fa fa-eye"></i>Download Doc</button></a>
         </div>`
                     }

else if(element.oi_status == 4 && element.oi_draft) {
let oi_draft = element.oi_draft.split('/').pop()
return `<div class="allactions__box">
<strong>Draft After Close OrderItem:</strong></br>
<a href="/console/queue/resumedownload/?path=${oi_draft}&next=${window.location.pathname}">
<button type="button" class="btn btn-success btn-xs">
<i class="fa fa-eye"></i>Download Doc</button></a></div>`
                                                      }

else if(element.oi_draft){
let oi_draft = element.oi_draft.split('/').pop()
return `<div class="allactions__box">
  <strong>Draft Level ${ element.draft_counter < maxDraft ? element.draft_counter:Final}:</strong></br>
  <a href=<a href="/console/queue/resumedownload/?path=${oi_draft}&next=${window.location.pathname}"><button type="button" class="btn btn-success btn-xs"><i class="fa fa-eye"></i>Download Doc</button></a>
</div>`
}
else if( element.linkedin && element.order_oio_linkedin != ""){
return `<div class="allactions__box">
<strong>Candidate Draft</strong></br>
<a href="/linkedin/dashboard-draft-download/${element.oi}/${element.id}" target="_blank">
<button type="button" class="btn btn-success btn-xs"><i class="fa fa-eye"></i>Download Draft</button></a>
<strong>Draft Level ${ element.draft_counter < maxDraft ? element.draft_counter :Final}:</strong></br>
<a href="/linkedin/linkedin-draft/${element.oi}/${element.id}" target="_blank">
<button type="button" class="btn btn-success btn-xs"><i class="fa fa-eye"></i>View Draft</button></a></div>`
}
}


function fileUploadForm(oiOperation){
   return ` <form autocomplete="off" role="form" method="post"  data-parsley-validate enctype="multipart/form-data" id="draft-upload-form${oiOperation.oi}">
         <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
           <input type="file" name="file" required="" id="id_file">
           <div style="display:none">
               <input type="hidden" name="oi_pk" value="${oiOperation.oi}">
               <input type="hidden" id="flow-id{oiOperation.oi}" name="flow" value="detailpage"/>
           </div>
           <button type="button" onclick="clickSubmitDraft('{oiOperation.oi}',)" class="btn btn-success btn-xs">Submit</button>
           </form>


      <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-hidden="true" id="draftmodal${oiOperation.oi}">
                         <div class="modal-dialog modal-lg">
                           <div class="modal-content">

                             <div class="modal-header">
                               <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span>
                               </button>
                               <h4 class="modal-title" id="myModalLabel">Draft Upload</h4>
                             </div>

                             <div class="modal-body" id="myModalbody${oiOperation.oi}">
                               Are You Sure???
                             </div>

                             <div class="modal-footer">
                               <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                               <button type="button" id="uploadDraftAction${oiOperation.oi} data-dismiss="modal" class="btn btn-primary" onclick="detailPageUploadDraft('${oiOperation.oi}',)">Yes</button>
                             </div>

                           </div>

                         </div>

                       </div>`


}




function allActionModal(id){
  $('#orderItemOperationModal').html('')
$.get( "/order/api/v1/orderitemoperationsapi/", { 'oi': id ,'nopage':true,'include_oi_id':true} )
  .done(function( data ) {
    if(data ){
    let result = ""
    for (oiOperation of data){

      result += `<div class="allactions__box">
                <p>${oiOperation.oi_status_display}</p>
          <span>${new Date(oiOperation.created).toDateString()}</span>
          </div>
    ${createDraftResumeDownload(oiOperation)? createDraftResumeDownload(oiOperation):''}
    ${ (oiOperation.oi_status == 4) ? (oiOperation.oi_id_data.oi_draft_path || oiOperation.linkedin) ?
          fileUploadForm(oiOperation)
        :'':'' }

    } }
    `
    }
    $('#orderItemOperationModal').html(result);
}
$('#loader').hide();
  });

}
function allMessage(id){
  $('#orderItemOperationModal').html('')
$.get( "/order/api/v1/message-communications/", { 'oi': id ,'nopage':true} )
  .done(function( data ) {
  debugger;
    if(data){
    let result = ""
    $('#MessageCounts').text('All Messages (' + data.length + ')');
    for (msg of data){
       result += `   <div class="allmessages__box">
          <p>${msg.message}</p>
          <span>
              <strong>${msg.added_by_name}</strong>
             ${new Date(msg.created).toDateString()}</span>
        </div>`
    }
    $('#MessagesModal').html(result);
}
$('#message-loader').hide();
  });

}