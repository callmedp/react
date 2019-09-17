$(document).ready(function() {
    $('.date-range-picker').daterangepicker({
        autoUpdateInput: false,
        locale: {
          format: 'DD/MM/YYYY',
          cancelLabel: 'Clear',
        },
        maxDate: moment().endOf("day"),
    },function(start, end, label) {
      
    });

    $('.date-range-picker').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
    });

    $('.date-range-picker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    })

    $('#id_filter').click(function(){
        $('#list-filter-form').submit();
    });

});

function sort(){
      if($('#sort_type').val() == 'delivery_speed'){
        $('#delivery_form').submit();
      }
      else if($('#sort_type').val() == 'Date'){
        $('#date_form').submit();
      }
      else if($('#sort_type').val() == 'payment_date'){
        $('#payment_date_form').submit();
      }
    };