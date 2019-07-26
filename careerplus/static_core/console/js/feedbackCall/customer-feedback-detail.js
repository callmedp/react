let category = {},resolution = {},total_order_item = 0,total_pages_operations=0,page_size=5
let form_data = {
    IsFollowUp:false
}
let current_index = -1

function createDropdown(id,data,pre_value){
    for (item in data){
        $(`#${id}`).append(
            `
                <option value="${item}">${data[item]}</option>
            `
        )
    }
    if(pre_value)
        $(`#${id}`).val(`${pre_value}`);
}

$(document).ready(function() { 
    
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });


    $('#follow-up').datetimepicker()

    $.get(`/console/api/v1/feedback-call/feedback-detail/${id}/`,(data)=>{
        $('#customer-detail').empty()
        $('#customer-detail').append(
          `
            <tr class="even pointer">
              <td>${data.full_name}</td>
              <td>
                  <div>
                      <div id="customer-email">${data.email}</div>
                      <button type="button" class="btn btn-primary btn-xs" onclick="showData(this,'email')"><i class="fa fa-search" aria-hidden="true"></i>ClickToView</button>
                  </div>
              </td>
              <td>
                  <div>
                      <div id="customer-mobile">${data.mobile}</div>
                      <button type="button" class="btn btn-primary btn-xs" onclick="showData(this,'mobile')"><i class="fa fa-phone-square" aria-hidden="true"></i>ClickToView</button>
                  </div>
              </td>
              <td>${data.ltv_value}</td>
            </tr>
          `
        )
        if (data.status === 3){ //closed feedback call
            $('#add-order-item-feedback').hide()
            $('#close-feedback').hide()
            $('#set-follow-up').hide()
        }
        $('#feedback-comment').val(data.comment)
        form_data['comment'] = data.comment
        form_data['follow-up'] = data.follow_up_date
    })

    $.get(`/console/api/v1/feedback-call/dropdown-choices/`,(data)=>{
        if(data.category){
            category = data.category
            createDropdown('category-choices',category)
        }
        if(data.resolution){
            resolution = data.resolution
            createDropdown('resolution-choices',resolution)
        }
    })

    $.get(`/console/api/v1/feedback-call/feedback/${id}/order-items/`,{
        'include_order_item_id':true
    },(data)=>{
        total_order_item = data.count
        if(data.results){
            for (index in data.results){
                let item = data.results[index]
                let order_item = item.order_item_id_data
                $('#order-item-entries').append(
                    `
                        <tr class="even pointer">
                            <td class="padding-item">${order_item.length ? order_item[0].product_name : ''}item</td>
                            <td class="padding-item">${order_item.length ? order_item[0].order_status_text : ''}</td>
                            <td class="padding-item">${item.order_item}</td>
                            <td class="padding-item">${order_item.length ? order_item[0].order_payment_date : ''}</td>
                            <td class="scalling">
                                <select id="item-category-${index}" onclick="removeError('#item-category-${index}',${index},'category')" name="resolution" class="form-control">
                                    <option value="">Select Category</option>
                                </select>
                                <span class="help-block hide">Select a Category</span>
                            </td>
                            <td class="scalling"> 
                                <select id="item-resolution-${index}" onclick="removeError('#item-resolution-${index}',${index},'resolution')" name="resolution" class="form-control">
                                    <option value="">Select Resolution</option>
                                </select>
                                <span class="help-block hide">Select a Resolution</span>
                            </td>
                            <td class="padding-item"><button class="btn btn-primary review-button" onclick="openModal(${index})"><i class="fa fa-edit edit-icon"></i>Write a review</button></td>
                        </tr> 
                    `
                )
                createDropdown(`item-category-${index}`,category,item.category)
                form_data[index] = {
                                        id: item.id,
                                        category: item.category,
                                        resolution: item.resolution,
                                        comment: item.comment,
                                    };
                createDropdown(`item-resolution-${index}`,resolution,item.resolution)
            }
        }
        
    })

    $('#category-choices').change(function(){ 
        var value = $(this).val();
        for(let order_item_index = 0;order_item_index<total_order_item;order_item_index++){
            $(`#item-category-${order_item_index}`).val(value)
            removeError(`#item-category-${order_item_index}`,order_item_index,'category')
        }
    });

    $('#resolution-choices').change(function(){ 
        var value = $(this).val();
        for(let order_item_index = 0;order_item_index<total_order_item;order_item_index++){
            $(`#item-resolution-${order_item_index}`).val(value)
            removeError(`#item-resolution-${order_item_index}`,order_item_index,'resolution')
        }
    });

    $('#follow-up').on('changeDate', function(ev){
        $(this).datetimepicker('hide');
    });

    getOrderItemFeedbackOperation(1)

})

function showData(button,type){
    $(button).hide()
    $(`#customer-${type}`).show()
}

function openModal(order_item_feedback_index){
    current_index = order_item_feedback_index 
    let comment = form_data[order_item_feedback_index].comment
    $('#order-item-message').removeClass('hide')
    $('#follow-up-div').addClass('hide')
    $('#order-item-message').val(comment ? comment : '')
    $('#review-modal').modal('show')
}

function saveReview(){
    $('#review-modal').modal('hide')
    if($('#order-item-message').hasClass('hide')){
        form_data['IsFollowUp'] = true
        form_data['follow-up'] = $('#follow-up').val()
        sendData()
    }
    else{
        form_data[current_index].comment = $('#order-item-message').val()
    }
    
}

function sendData(){
    $.post(`/console/api/v1/feedback-call/feedback/${id}/save-data/`,{
        form_data:JSON.stringify(form_data)
    },(data)=>{
        if(data.result){
            window.location = '/console/feedbackcall/queue/'
        }
    })
}


function submitFeedback(){
    if(!checkError()){
        sendData()
    }
}

function followUpFeedback(){
    if(!checkError()){
        $('#order-item-message').addClass('hide')
        $('#follow-up-div').removeClass('hide')
        $('#review-modal').modal('show')
    }
}

function checkError(){
    let error = false
    for(key in form_data){
        let item = form_data[key]
        if(item && typeof item === 'object'){ 
            if(!item.category){
                showError(`#item-category-${key}`);
                error=true
            }  
            if(!item.resolution){
                showError(`#item-resolution-${key}`);
                error=true
            }
        }
        else{
            if(key ==='comment' && !item){
                showError('#feedback-comment')
                error = true;
            }
        }
    }
    return error
}


function showError(id){
    let parent = $(id).parent()
    parent.addClass('has-error')
    parent.children('.help-block').removeClass('hide')
}

function removeError(id,key,type){
    let  parent = $(id).parent()
    parent.removeClass('has-error')
    parent.children('.help-block').addClass('hide')
    if(type)
        form_data[key][type] = $(id).val()
    else
        form_data[key] = $(id).val()

}

function getOrderItemFeedbackOperation(page_no){
    $.get(`/console/api/v1/feedback-call/feedback/${id}/operations/?page_size=${page_size}&page=${page_no}`,{
        'include_order_item_id':true
    },(data)=>{
        total_pages_operations = Math.ceil(data['count']/page_size)
        if(data.results){
            $('#ops-history-entries').empty()
            for (item of data.results){
                let order_item = item.order_item_id_data
                $('#ops-history-entries').append(
                    `
                        <tr class="even pointer">
                            <td class="padding-item">${item.assigned_to_text ? item.assigned_to_text : '-'}</td>
                            <td class="padding-item">${order_item.length ? order_item[0].product_name : ''}item</td>
                            <td class="padding-item">${item.added_on_date}</td>
                            <td class="padding-item">${item.category_text ? item.category_text : '-'}</td>
                            <td class="padding-item">${item.resolution_text ? item.resolution_text : '-'}</td>
                            <td class="padding-item">${item.comment ? item.comment : ''}</td>
                        </tr> 
                    `
                )
            }
        }
        $('#page-no').text(`Page ${total_pages_operations===0 ? 0: page_no} of ${total_pages_operations}`)
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
        for (let page=1;page<=total_pages_operations && page<=5;page++){
            $('.pagination').append(
                `
                    <li ${page===page_no ? "class='active'" : ''} ><a ${page===page_no ? '' :`onclick="getOrderItemFeedbackOperation(${page})"`}>${page}</a></li>
                `
            )
        }
        if (page_no !== total_pages_operations && total_pages_operations>0){
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


