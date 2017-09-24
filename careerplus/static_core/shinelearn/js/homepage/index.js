function redirectToSearch(e) {
    location.href = '/search/results/?q='+encodeURI($('#id_q').val())
}

jQuery(document).ready(function($) {
  $('#tags1').inputTags({
    // tags: ['jQuery'],
    autocomplete: {
      values: ['Pellentesque', 'habitant', 'morbi', 'tristique', 'senectus', 'netus', 'malesuada', 'fames', 'turpis', 'egestas', 'Vestibulum'],
      only: true
    },
    max: 1,
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
    // tags: ['jQuery', 'Python', 'Nass'],
    autocomplete: {
      values: ['Pellentesque', 'habitant', 'morbi', 'tristique', 'senectus', 'netus', 'malesuada', 'fames', 'turpis', 'egestas', 'Vestibulum'],
      only: true
    },
    max: 3,
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
    // $('#myCarousel1').carousel({
    //     interval: 10000
    //   });
    //
    //   $('.product-carousel .carousel .item').each(function(){
    //     var next = $(this).next();
    //     if (!next.length) {
    //       next = $(this).siblings(':first');
    //     }
    //     next.children(':first-child').clone().appendTo($(this));
    //
    //     if (next.next().length>0) {
    //       next.next().children(':first-child').clone().appendTo($(this));
    //     }
    //     else {
    //       $(this).siblings(':first').children(':first-child').clone().appendTo($(this));
    //     }
    //   });
});