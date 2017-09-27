function redirectToSearch(e) {
    location.href = '/search/results/?q='+encodeURI($('#id_q').val())
}

jQuery(document).ready(function($) {
    $('#tags1').inputTags({
        placeholder: prefetchedFuncArea ? '': "Select Functional Area",
        autocomplete: {
            values: funcAreaSet,
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
        placeholder: prefetchedSkills ? '': "Choose upto 3 Skills",
        autocomplete: {
            values: skillsSet,
            only: true
        },
        max: 3,
        create: function(e) {
            var $field = e.$input[0];
            $field.placeholder = '';
        },
        destroy: function(e) {
            var $field = e.$input[0];
            if (e.tags.length == 0)
            $field.placeholder = 'Choose upto 3 Skills';
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
});