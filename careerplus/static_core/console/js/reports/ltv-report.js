

$(document).ready(() => { 
    // $('.loader').show()
    // $('body').addClass('body-overflow')
    $('#report_date').datepicker({
        'format': "mm-yyyy",
        'viewMode': "months", 
        'startDate':"07-2018",
        'endDate':'today',
        'autoclose':true,
        'minViewMode': "months"
    });
    $('#report_date').val(getDefaultDate())

    
    getLTVRecords()

})

const getDefaultDate = ()=>{
    var todayDate = new Date();
    return `${todayDate.getMonth()+1}-${todayDate.getFullYear()}`
}

const getLTVRecords = (year,month) =>{
    date = $('#report_date').val()
    year = date.split('-')[1]
    month = date.split('-')[0]
    //loader
    $('.loader').show()
    $('body').addClass('body-overflow')

    $.get(`/order/api/v1/ltv-report/${year}/${month}`,(data)=>{
        
        $('#messages').empty()
        if(data.count === 0){
            $('#messages').append(
                `
                    <div  class="alert alert-error alert-dismissable">
                        No record
                    </div>
                `
            )
            $('.export-csv').hide()
            $('#ltv-records').empty()
        }

        if(data.results && data.count){
            $('.export-csv').show()
            $('#ltv-records').empty()
            for (result of data.results){
                $('#ltv-records').append(
                    `
                        <tr class="even pointer">
                            <td>${result.ltv_bracket_text}</td>
                            <td>${result.total_users}</td>
                            <td>${result.total_order_count}</td>
                            <td>${result.total_item_count}</td>
                            <td>${result.crm_users} (${result.crm_order_count})</td>
                            <td>${result.crm_item_count}</td>
                            <td>${result.learning_users} (${result.learning_order_count})</td>
                            <td>${result.learning_item_count}</td>
                            <td>${result.revenue}</td>
                        </tr>
                    `
                )
            }
            
        }

        // end loader
        $('.loader').hide()
        $('body').removeClass('body-overflow')
        
    }).fail(()=>{
        $('#messages').empty()
        $('#messages').append(
            `
                <div  class="alert alert-error alert-dismissable">
                    Something went wrong
                </div>
            `
        )
        // stop loader
        $('.loader').hide()
        $('body').removeClass('body-overflow')
    })
}

const generateReport = () =>{
    $('#ltv-report-form').empty()
    $('#ltv-report-form').append(
        `
            ${csrfTokenInput}
            <input id="date" type="hidden" name="date" value=${$('#report_date').val()}>
            <button type="button" class="btn btn-primary export-csv"onclick="generateReport()"
                        >Export to CSV</button>
                    
        `
    )
    $('#ltv-report-form').submit()
}


