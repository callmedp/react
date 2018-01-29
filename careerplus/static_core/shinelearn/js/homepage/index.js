/*
function redirectToSearch(e) {
    var $q = $('#id_q');
    if ($q.val()) {
        $q.closest('div').removeClass('error-search');
        $q.closest('div').find('.error-txt').html();
        location.href = '/search/results/?q='+encodeURI($q.val());
    }
    else {
        $q.closest('div').addClass('error-search');
        $q.closest('div').find('.error-txt').html('Please enter a query');
        return false;
    }
};
*/

$(document).ready(function($) {
    
    $('#tags1').inputTags({
        placeholder: prefetchedFuncArea ? '': "Select Functional Area",
        autocomplete: {
            values: funcAreaSet,
            actualValues: funcAreaSet,
            only: true
        },
        max: 1,
        maxLength: 100,
        create: function(e) {
            var $field = e.$input[0];
            $field.placeholder = '';
        },
        destroy: function(e) {
            var $field = e.$input[0];
            if (e.tags.length == 0)
            $field.placeholder = 'Select Functional Area';
        },
        errors: {
            empty: "Be careful, you can't add an empty tag.",
            minLength: 'Your tag must have at least %s characters.',
            maxLength: 'Your tag must not exceed %s characters.',
            max: 'Please note that the number of tags must not exceed %s.',
            email: 'The email address you entered is not valid',
            exists: 'This tag already exists',
            autocomplete_only: 'You must select a value from the list.',
            timeout: 8000
        }
    });

    $('#tags2').inputTags({
        placeholder: prefetchedSkills ? '': "Choose upto 2 Skills",
        autocomplete: {
            values: skillsSet,
            actualValues: skillsSet,
            only: true
        },
        max: 2,
        maxLength: 100,
        create: function(e) {
            var $field = e.$input[0];
            $field.placeholder = '';
        },
        destroy: function(e) {
            var $field = e.$input[0];
            if (e.tags.length == 0)
            $field.placeholder = 'Choose upto 2 Skills';
        },
        errors: {
            empty: "Be careful, you can't add an empty tag.",
            minLength: 'Your tag must have at least %s characters.',
            maxLength: 'Your tag must not exceed %s characters.',
            max: 'Please note that the number of tags must not exceed %s.',
            email: 'The email address you entered is not valid',
            exists: 'This tag already exists',
            autocomplete_only: 'You must select a value from the list.',
            timeout: 8000
        }
    });
    // Header Scroll
      $(window).on('scroll', function() {
          var scroll = $(window).scrollTop();

          if (scroll >= 50) {
              $('.navbar').addClass('navbar-color');
          } else {
              $('.navbar').removeClass('navbar-color');
          }
      });


    /*$('.key_press_js_search').keypress(function (e) {
        if (e.which == 13) {
            redirectToSearch();
            return false; 
        }
    });*/
    
    $('.js_advance_search').on('click', function (e) {
        e.preventDefault();
        var flag1 = true,
            flag2 = true;
        var $tags1 = $('#tags1'),
            $tags2 = $('#tags2');
            if (!$tags1.val()){
                flag1 = false;
                $tags1.closest('div').addClass('error-search');
                $tags1.siblings('.error-txt').html('Please choose a functional area.');
            }
            else {
                flag1 = true;
                $tags1.closest('div').removeClass('error-search');
                $tags1.siblings('.error-txt').html('');
            }
            if (!$tags2.val()){
                flag2 = false;
                $tags2.closest('div').addClass('error-search');
                $tags2.siblings('.error-txt').html('Please choose a skill.');
            }
            else {
                flag2 = true;
                $tags2.closest('div').removeClass('error-search');
                $tags2.siblings('.error-txt').html('');
            }
            if (flag2 && flag1) {
                $(".js_advance_search_form").submit();
            }
    });
    $('.tt-query').css('background-color','#fff');


    


});