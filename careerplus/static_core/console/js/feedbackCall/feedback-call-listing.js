//global variables
let page_size = 10
let total_pages = 0
let feedback_id_selected = []


$(document).ready(() => { 
    $('#filter-status').val('1') //default Status  dopdown selected to Pending   (Requirement from Product)

    $('#feedback-type').val('1') //default Feedback Type dropdown selected to Fresh (Requirement from Product)
    
    $('.feedback_users').select2({    //create searchable dropdown
        width:'100%',
    });

    customerFeedbackList(1)
    getUsers()

    $('#check-all').click((e) => {      //select all feedback on page
        $(this).closest('table').find('td input:checkbox').prop('checked', this.checked);
        feedback_id_selected = []
        $('#body-table-list input[name="table_records"]:checked').each(() => {
            feedback_id_selected.push(parseInt($(this).prop('value')));
        });
    });

    $('#filter-status').change(()=>{
        customerFeedbackList(1)
    })
    $('#feedback-type').change(()=>{
        customerFeedbackList(1)
    })

    $('#filter-follow-up').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD'
        }
      }).val('');
    $('#filter-added-on').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD'
        }
      }).val('');
    
});


const getUsers = () => {
    $.get(`/user/api/v1/get-users/`,{
        'group':'welcome_call',
        'active':true
    },(data)=>{
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
            $('#filter-user').append(
                `
                <option value='${user.id}'>${user.name}</option>
                `
            )
        }
    })
}


const customerFeedbackList = (page_no,filter_data) => {
    //add loader
    $('.feedback-loader').show()
    $('body').addClass('body-overflow') //remove scrolling while loading

    status = $('#filter-status').val()
    status === '3' ? $('#assign-user-form').hide() : $('#assign-user-form').show()

    filter_update_data = {
        search_text:$('#search-box').val(),
        page_size:page_size,
        page:page_no,
        status:status,
        type:$('#feedback-type').val(),
    }
    if(filter_data){
        filter_update_data = Object.assign({},filter_update_data,filter_data)
    }
    $.get(`/console/api/v1/feedback-call/customer-list/`,
    filter_update_data,
    (data)=>{
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
                            <td>${formatDate(result.added_on)}</td>
                            <td>${result.follow_up_date ? formatDate(result.follow_up_date,true) : '-'}</td>
                            <td>${result.status_text}</td>
                            <td>${formatDate(result.last_payment_date)}</td>
                            <td>${result.assigned_to_text ? result.assigned_to_text : '-'}</td>
                            <td><a><button type="button" class="btn btn-primary btn-xs" onclick="redirectFeedbackUpdatePage(${result.id})">Update</button></a></td>
                        </tr>
                    `
                )
            }
        }
        total_pages = Math.ceil(data['count']/page_size)
        $('#page-no').text(`Page ${total_pages===0 ? 0: page_no} of ${total_pages}`)
        $('.pagination').empty()
        if (page_no !== 1){
            $('.pagination').append(
                `
                    <li>
                        <a onclick="customerFeedbackList(${page_no -1})" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                `
            )
        }
        for (let page=1;page<=total_pages && page<=5;page++){
            $('.pagination').append(
                `
                    <li ${page===page_no ? "class='active'" : ''} ><a ${page===page_no ? '' :`onclick="customerFeedbackList(${page})"`}>${page}</a></li>
                `
            )
        }
        if (page_no !== total_pages && total_pages>0){
            $('.pagination').append(
                `
                    <li>
                        <a onclick="customerFeedbackList(${page_no +1})" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                `
            )
        }
        // loader remove
        $('.feedback-loader').hide()
        $('body').removeClass('body-overflow')
        
    })
    
}

const uncheckAll = (checkbox,id) => {
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


const assignFeedbackIdsUser = () => {
    user_id =$('.feedback_users').find(':selected').val();
    if(!user_id || feedback_id_selected.length===0){
        alert(`${!user_id ?'Select user id': 'Select Customer feedback'} to continue`)
        return
    }   
    $('.feedback-loader').show()
    $('body').addClass('body-overflow') //remove scrolling while loading
    $.post(`/console/api/v1/feedback-call/assign-feedback-call/`,{
        'feedback_ids':JSON.stringify(feedback_id_selected),
        'user_id':user_id
    },(data)=>{
        if(data.result){
            $('.feedback_users').val('')
            $('.feedback_users').trigger('change.select2');
            customerFeedbackList(1)
            
        }
    })
}


const filterFeedbackList = () => {
    filter_data ={
        follow_up_date_range : $('#filter-follow-up').val(),
        added_on_range : $('#filter-added-on').val(),
        user : $('#filter-user').val()
    }
    customerFeedbackList(1,filter_data)

}

const redirectFeedbackUpdatePage = (id) => {
    window.location.href = `/console/feedbackcall/update/${id}`
}




const searchNameOrEmail = () => {
    $('#filter-status').val('')
    $('#feedback-type').val('')
    customerFeedbackList(1)
}

const searchBoxKeyEnter = (event) =>{
    if (event.keyCode == 13 || event.which == 13){
        searchNameOrEmail()
    }
}

const removeDate = (id)=>{
    $(id).val('')
}

