function redirectToSearch(e) {
    location.href = '/search/results/?q='+encodeURI($('#id_q').val())
}

jQuery(document).ready(function($) {
    
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


    $('.key_press_js_search').keypress(function (e) {
        if (e.which == 13) {
            redirectToSearch();
            return false; 
        }
    });
    
    // $('.js_advance_search').on('click', function () {
    //     debugger;
    //     var flag = true;
    //         if (!$('#tags1').val()){
    //             flag = false;
    //             $('#tags1').siblings('.error').html('Please choose a functional area.');
    //         }
    //         if (!$('#tags2').val()){
    //             flag = false;
    //             $('#tags2').siblings('.error').html('Please choose a skill.');
    //         }
    //         console.log(flag);
    //         console.log($('#tags1').val());
    //         console.log($('#tags2').val());
    //     debugger;
    //         if (flag) {
    //             debugger;
    //             $(".js_advance_search_form").submit();
    //         }    
    // });
    
    
        $('#tags1').change(function(){
            if ($('#tags1').val()){
                $('#tags1').siblings('.error').html('');
            }
        });
 
});