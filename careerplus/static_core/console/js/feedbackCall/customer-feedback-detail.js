//global variables
let category = {results:[]},resolution = {results:[]},total_order_item = 0,total_pages_operations=0,page_size=5
let form_data = {
    IsFollowUp:false
}
let current_index = -1
let first_error_id = null

//fuunctions called when page loads
$(document).ready(() => { 
    //add loader
    $('.feedback-loader').show()
    $('body').addClass('body-overflow') //remove scrolling while loading

    let one_day_followUp_date = new Date()
    let seven_days_followUp_date = new Date();
    one_day_followUp_date.setDate(one_day_followUp_date.getDate() + 1);
    seven_days_followUp_date.setDate(seven_days_followUp_date.getDate() + 7);

    $('#follow-up').val(formatDate(seven_days_followUp_date,true))


    $('#follow-up').datetimepicker({
        startDate: new Date(),
        setDate: new Date()
    }) //make input fild datetime
    feedbackCallDetails()
    getDropdownChoices()

    $('#category-choices').on('select2:select', function (e) { //detect change in category dropdown choices
        var value = $(this).val();
        for(let order_item_index = 0;order_item_index<total_order_item;order_item_index++){
            $(`#item-category-${order_item_index}`).val(value)
            $(`#item-category-${order_item_index}`).trigger('change.select2');
            removeError(false,{id:`#item-category-${order_item_index}`,key:order_item_index,type:'category'},true)
        }
        if (value === '201'){
            $('#follow-up').val(formatDate(one_day_followUp_date,true))
        }
        else{
            $('#follow-up').val(formatDate(seven_days_followUp_date,true))
        }
    });

    $('#resolution-choices').on('select2:select', function (e) { //detect change in resolution dropdown choices
        var value = $(this).val();
        for(let order_item_index = 0;order_item_index<total_order_item;order_item_index++){
            $(`#item-resolution-${order_item_index}`).val(value)
            $(`#item-resolution-${order_item_index}`).trigger('change.select2');
            removeError(false,{id:`#item-resolution-${order_item_index}`,key:order_item_index,type:'resolution'},true)
        }
    });

    $('#follow-up').on('changeDate', function(ev){  //hide datetimepicker when date is selected
        $(this).datetimepicker('hide');
    });

    $('#oi-type-choices').val('');

    $('#oi-type-choices').change(()=>{
        getOrderItemFeedbackOperation(1)
    })

    
    
    getOrderItemFeedbackOperation(1)

})


const feedbackCallDetails = () => {
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
              <td>${data.ltv ? data.ltv : 0}</td>
            </tr>
          `
        )
        if (data.status === 3){  //closed feedback call so hide forms
            $('#add-order-item-feedback').hide()
            $('#close-feedback').hide()
            $('#set-follow-up').hide()
        }
        $('#feedback-comment').val(data.comment)
        form_data['comment'] = data.comment
        form_data['follow-up'] = data.follow_up_date
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'Feedback call details not loaded'
        })
    })
}

const getOrderItemFeedback = () => {
    $.get(`/console/api/v1/feedback-call/feedback/${id}/order-items/`,{
        'include_order_item_id':true,
        'nopage':true
    },(data)=>{
        total_order_item = data.count
        if(data.results){
            for (index in data.results){
                let item = data.results[index]
                let order_item = item.order_item_id_data
                $('#order-item-entries').append(
                    `
                        <tr class="even pointer">
                            <td class="padding-item">${order_item.length ? order_item[0].product_name : ''}</td>
                            <td class="padding-item">${order_item.length ? order_item[0].get_oi_status : ''}</td>
                            <td class="padding-item"><a class="orderitem-id" href="/console/queue/order/${order_item.length ? order_item[0].order_id : ''}/details/">${item.order_item}</a></td>
                            <td class="padding-item">${order_item.length ? formatDate(order_item[0].order_payment_date) : ''}</td>
                            <td class="scalling">
                                <select id="item-category-${index}" onclick="removeError('#item-category-${index}',${index},'category')" name="category" class="form-control">
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
                createDropdown(`#item-category-${index}`,category,index,'category',item.category)
                form_data[index] = {
                                        id: item.id,
                                        category: `${item.category ? item.category : ''}`,
                                        resolution: `${item.resolution ? item.resolution : ''}`,
                                        comment: item.comment,
                                    };
                createDropdown(`#item-resolution-${index}`,resolution,index,'resolution',item.resolution)
            }
        }
        // loader remove
        $('.feedback-loader').hide()
        $('body').removeClass('body-overflow')
        
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'OrderItem feedabcks not loaded'
        })
    })

}

const getDropdownChoices = () => {
    $.get(`/console/api/v1/feedback-call/category-choices/`,(data)=>{
        if(data){
            category = data
            createDropdown('#category-choices',category,null,null,null,true)
            $.get(`/console/api/v1/feedback-call/resolution-choices/`,(data)=>{
                if(data){
                    resolution = data
                    createDropdown('#resolution-choices',resolution,null,null,null,true)
                    getOrderItemFeedback()
                }
            }).fail(()=>{
                Toast.fire({
                    type: 'error',
                    title: 'Resolution Choice not loaded'
                })
            })
        }
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'Category CHoice not loaded'
        })
    })
    
}


const createDropdown  = (id,data,index,type,pre_value,isMainDropdown) => {
    properties = {
        data:data,
        minimumResultsForSearch: -1,
    }
    isMainDropdown ? ()=>{} : properties['width']='160px'  
    $(id).select2(properties);
    $(id).on('select2:select', {id:id,key:index,type},removeError);
    if (pre_value){
        $(id).val(pre_value)
        $(id).trigger('change.select2');
    }

}

const showData = (button,type) => {
    $(button).hide()
    $(`#customer-${type}`).show()
}

const openModal = (order_item_feedback_index) => {
    current_index = order_item_feedback_index 
    let comment = form_data[order_item_feedback_index].comment
    $('#order-item-message').parent().removeClass('hide')
    $('#follow-up-div').addClass('hide')
    $('#order-item-message').val(comment ? comment : '')
    $('#review-modal').modal('show')
}

const saveReview = () => {
    $('#review-modal').modal('hide')
    if($('#order-item-message').parent().hasClass('hide')){
        form_data['IsFollowUp'] = true
        form_data['follow-up'] = $('#follow-up').val()
        sendData('Follow Up')
    }
    else{
        form_data[current_index].comment = $('#order-item-message').val()
    }
    
}

const sendData = (type) => {
    // loader show
    $('.feedback-loader').show()
    $('body').addClass('body-overflow')

    $.post(`/console/api/v1/feedback-call/feedback/${id}/save-data/`,{
        form_data:JSON.stringify(form_data)
    },(data)=>{
        if(data.result){    
            Toast.fire({
                type: 'success',
                title: 'Feedback Saved Succesfully'
            })
            window.location = '/console/feedbackcall/queue/'
        }
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'Feedback not Saved'
        })
    })
}


const submitFeedback = () => {
    if(!checkError()){
        sendData('Feedback')
    }
    else{
        $("html, body").animate({ scrollTop: $(`${first_error_id}`).offset().top -100 }, 1000);
    }
}

const followUpFeedback = () => {
    if(!checkError()){
        $('#order-item-message').parent().addClass('hide')
        $('#follow-up-div').removeClass('hide')
        $('#review-modal').modal('show')
    }
    else{
        $("html, body").animate({ scrollTop: $(`${first_error_id}`).offset().top -100 }, 1000);
    }
}

const checkError = () => {
    let error = false
    for(key in form_data){
        let item = form_data[key]
        if(item && typeof item === 'object'){ 
            if(!item.category){
                showError(`#item-category-${key}`);
                error=true
            }  
            else if(item.category === '201'){   //not connected id
                $(`#item-resolution-${key}`).val('')
                $(`#item-resolution-${key}`).trigger('change.select2');
                removeError(false,{id:`#item-resolution-${key}`,key,type:'resolution'},true)
                continue;
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


const showError = (id) => {
    first_error_id = first_error_id ? first_error_id : id
    let parent = $(id).parent()
    parent.addClass('has-error')
    parent.children('.help-block').removeClass('hide')
}

const removeError = (event,data,isMainDropdown) => {
    first_error_id = null
    let id,key,type;
    if(event){
        id = event.data.id
        key = event.data.key
        type = event.data.type
    }
    else{
        id = data.id,
        key = data.key,
        type = data.type
    }
    let  parent = $(id).parent()
    parent.removeClass('has-error')
    parent.children('.help-block').addClass('hide')
    if(type)
        form_data[key][type] = $(id).val() ? $(id).val() : null
    else
        form_data[key] = $(id).val()
    if(form_data[key].category === '201'){  //make resolution null as not connected selected
        $(`#item-resolution-${key}`).val('')
        $(`#item-resolution-${key}`).trigger('change.select2');
        $(`#item-resolution-${key}`).prop('disabled', true)
        return
    }
    else{
        $(`#item-resolution-${key}`).prop('disabled', false)
    }
    

}

const getOrderItemFeedbackOperation = (page_no) => {
    prev_loader = false
    if($('.feedback-loader:visible').length == 0){
        $('.feedback-loader').show()
        $('body').addClass('body-overflow') //remove scrolling while loading
    }
    else
        prev_loader = true
    

    $.get(`/console/api/v1/feedback-call/feedback/${id}/operations/?page_size=${page_size}&page=${page_no}`,{
        'include_order_item_id':true,
        'oi_type': $('#oi-type-choices').val()
    },(data)=>{
        total_pages_operations = Math.ceil(data['count']/page_size)
        if(data.results){
            $('#ops-history-entries').empty()
            for (key in data.results){
                let item = data.results[key]
                let order_item = item.order_item_id_data
                $('#ops-history-entries').append(
                    `
                        <tr class="even pointer">
                            <td class="padding-item">${item.assigned_to_text ? item.assigned_to_text : '-'}</td>
                            <td class="padding-item">${order_item.length && order_item[0].product_name ? order_item[0].product_name : '-'}</td>
                            <td class="padding-item">${item.oi_type_text}</td>
                            <td class="padding-item">${formatDate(item.added_on,true)}</td>
                            <td class="padding-item">${item.category_text ? item.category_text : '-'}</td>
                            <td class="padding-item">${item.resolution_text ? item.resolution_text : '-'}</td>
                            <td class="padding-item"><div id="operation-comment-${key}" class="truncate">${item.comment ? item.comment : ''}</div>${item.comment ? `<a class="view-more" onclick="viewMore('#operation-comment-${key}',this)">Show More</a>` : ''}</td>
                        </tr> 
                    `
                )
            }
        }
        total_pages_operations ?  $('#page-no').text(`Page ${page_no + ' '}of ${total_pages_operations}`): $('#page-no').text('')
        $('.pagination').empty();
        if (page_no !== 1){
            $('.pagination').append(
                `
                    <li>
                        <a onclick="getOrderItemFeedbackOperation(${page_no -1})" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                `
            )
        }
        max_page = page_no>2 ? page_no+3 : page_no+6 -page_no
        for (let page=page_no>2 ? page_no-2 : 1;page<=total_pages_operations && page< max_page;page++){
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
                        <a onclick="getOrderItemFeedbackOperation(${page_no +1})" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                `
            )
        }
        if(!prev_loader){
            $('.feedback-loader').hide()
            $('body').removeClass('body-overflow') //remove scrolling while loading
        }
    }).fail(()=>{
        Toast.fire({
            type: 'error',
            title: 'OrderItem Feedback Operations not loaded'
        })
    })
}

const viewMore = (id,viewMoreElement)=>{
    $(id).toggleClass('truncate')
    if($(id).hasClass('truncate')){
        $(viewMoreElement).text('Show More')
    }
    else{
        $(viewMoreElement).text('Show Less')
    }
}


