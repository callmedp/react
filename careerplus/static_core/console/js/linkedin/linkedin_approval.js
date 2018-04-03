$(document).ready(function() {
    $('.date-range-picker').daterangepicker({
        autoUpdateInput: false,
        locale: {
          format: 'DD/MM/YYYY',
          cancelLabel: 'Clear',
        },
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