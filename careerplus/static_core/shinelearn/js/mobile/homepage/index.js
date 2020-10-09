function redirectToSearch(e) {
    var $q = $('#id_q');
    if ($q.val()) {
        $q.closest('div').removeClass('error');
        $q.closest('div').find('.error-txt').html();
        location.href = '/search/results/?q='+encodeURI($q.val());
    }
    else {
        $q.closest('div').addClass('error');
        $q.closest('div').find('.error-txt').html('Please enter a query');
        return false;
    }
}

$(document).ready(function () {
   $('.js_advance_search').on('click', function (e) {
        e.preventDefault();
        var flag1 = true,
            flag2 = true;
        var $tags1 = $('#tags11'),
            $tags2 = $('#tags21');
            if (!$tags1.val()){
                flag1 = false;
                $tags1.closest('div').addClass('error');
                $('.js_area_error').html('Please choose a functional area.');
            }
            else {
                flag1 = true;
                $tags1.closest('div').removeClass('error');
                $('.js_area_error').html('');
            }
            if (!$tags2.val()){
                flag2 = false;
                $tags2.closest('div').addClass('error');
                $('.js_skill_error').html('Please choose a skill.');
            }
            else {
                flag2 = true;
                $tags2.closest('div').removeClass('error');
                $('.js_skill_error').html('');
            }
            if (flag2 && flag1) {
                $(".js_advance_search_form").submit();
            }
    });


    // $('.key_press_js_search').keypress(function (e) {
    //     console.log(e.which);
    //     if (e.which == 13) {
    //         redirectToSearch();
    //         return false; 
    //     }
    // });

    $(document).on('keypress', '.key_press_js_search', function(e){
        var code = e.keyCode || e.which;
        if (code == 9 || code == 13 || code == 229) {
            redirectToSearch();
            return false; 
        }
    });
        WebFont.load({
            google: {
              families: ['Open+Sans:300,400,600,700']
            }
          });


});