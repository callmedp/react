let category = {},resolution = {}

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
    $.get(`/console/api/v1/feedback-call/feedback-detail/${id}`,(data)=>{
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
              <td>${data.ltv}</td>
            </tr>
          `
        )
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
        if(data.results){
            for (index in data.results){
                item = data.results[index]
                let order_item = item.order_item_id_data
                $('#order-item-entries').append(
                    `
                        <tr class="even pointer">
                            <td class="padding-item">${order_item.length ? order_item[0].product_name : ''}item</td>
                            <td class="padding-item">${order_item.length ? order_item[0].order_status_text : ''}</td>
                            <td class="padding-item">${item.order_item}</td>
                            <td class="padding-item">${order_item.length ? order_item[0].order_payment_date : ''}</td>
                            <td>
                            <select id="item-category-${index}" required="required" name="resolution" class="form-control">
                                <option value="">Select Category</option>
                            </select>
                            </td>
                            <td>
                            <select id="item-resolution-${index}" required="required" name="resolution" class="form-control">
                                <option value="">Select Resolution</option>
                            </select>
                            </td>
                        </tr> 
                    `
                )
                createDropdown(`item-category-${index}`,category,item.category)
                createDropdown(`item-resolution-${index}`,resolution,item.resolution)
            }
        }
        
    })
})

function showData(button,type){
    $(button).hide()
    $(`#customer-${type}`).show()
}

