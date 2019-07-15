let page_size = 5
let total_pages = 0

function update_feedback(id){
    window.location.href = `/console/feedbackcall/update/${id}`
}

$(document).ready(function() { 
    customerList(1)
    $.get(`/user/api/v1/get-users/`,{
        'group':'welcome_call',
        'active':true
    },(data)=>{
        console.log(data)
    })
    
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
                                <input autocomplete="off" type="checkbox" class="flat" name="table_records" value="${result.id}" >
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