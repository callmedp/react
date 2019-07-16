let page_size = 5
let total_pages = 0
let feedback_id_selected = []

function update_feedback(id){
    window.location.href = `/console/feedbackcall/update/${id}`
}

$(document).ready(function() { 
    $('.feedback_users').select2({
        width:'100%',
    });
    customerList(1)
    $.get(`/user/api/v1/get-users/`,{
        'group':'welcome_call',
        'active':true
    },(data)=>{
        console.log(data)
        $('.feedback_users').empty()
        $('.feedback_users').append(
            `
            <option value="">Select User</option>
            `
        )
        for (user of data['results']){
            $('.feedback_users').append(
                `
                <option value='${user.id}'>${user.name}(${user.email})</option>
                `
            )
        }
    })

    $('#check-all').click(function(e){      
        $(this).closest('table').find('td input:checkbox').prop('checked', this.checked);
        feedback_id_selected = []
        $('#body-table-list input[name="table_records"]:checked').each(function() {
            feedback_id_selected.push(parseInt($(this).prop('value')));
        });
    });
    
});


function customerList(page_no){
    $.get(`/console/api/v1/feedback-call/customer-list/?page_size=${page_size}&page=${page_no}`,(data)=>{
        if (data['results']){
            $('#body-table-list').empty()
            for (result of data['results']){
                $('#body-table-list').append(
                    `
                        <tr class="even pointer">
                            <td class="a-center ">
                                <input autocomplete="off" type="checkbox" class="flat" name="table_records" onclick="uncheckAll(this,${result.id})" value="${result.id}" >
                            </td>
                            <td>${result.full_name}</td>
                            <td>${result.added_on}</td>
                            <td>${result.follow_up_date}</td>
                            <td>${result.status_name}</td>
                            <td>${result.last_payment_date}</td>
                            <td>${result.assigned_to}</td>
                            <td><a><button type="button" class="btn btn-primary btn-xs" onclick="update_feedback(${result.id})">Update</button></a></td>
                        </tr>
                    `
                )
            }
        }
        total_pages = Math.ceil(data['count']/page_size)
        $('#page-no').text(`Page ${page_no} of ${total_pages}`)
        $('.pagination').empty()
        if (page_no !== 1){
            $('.pagination').append(
                `
                    <li>
                        <a onclick="customerList(${page_no -1})" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                `
            )
        }
        for (let page=1;page<=total_pages && page<=5;page++){
            $('.pagination').append(
                `
                    <li ${page===page_no ? "class='active'" : ''} ><a ${page===page_no ? '' :`onclick="customerList(${page})"`}>${page}</a></li>
                `
            )
        }
        if (page_no !== total_pages){
            $('.pagination').append(
                `
                    <li>
                        <a onclick="customerList(${page_no +1})" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                `
            )
        }
        
    })
    
}

function uncheckAll(checkbox,id){
   if($('#check-all')[0].checked && !checkbox.checked){
        $('#check-all').attr('checked',false)
   }
   if(checkbox.checked){
       feedback_id_selected.push(id)
   }
   else{
       feedback_id_selected.splice(feedback_id_selected.indexOf(id),1)
   }

}


function assignFeedbackIdsUser(){
    user_id =$('.feedback_users').find(':selected').val();
    if(!user_id || feedback_id_selected.length===0)
        return
    $.post(`/console/api/v1/feedback-call/assign-feedback-call/`,{
        'feedback_ids':JSON.stringify(feedback_id_selected),
        'user_id':user_id
    },(data)=>{
        console.log(data);
    })
}