function clicked() {
  $('.rmv-required').removeAttr('required')
  var check = confirm('Do you wish to Save the changes made - Y/N ?')
  if (check) {
    $("#linkedin-draft-form").submit();
  } else {
      return false;
  }
}
window.Parsley.addValidator('validatedate', {
  validateString: function(value, requirement, parsleyInstance) {
    var dcd = requirement.split("_")[1]
    var form_type = requirement.split("_")[0]
    var state_var = (form_type=="work") ? "org_current" : "edu_current"
    var curr_state

    if(dcd == 'from'){
      to_date = new Date(value)
      from = parsleyInstance.$element[0].id.replace(requirement.replace('from', 'to'),requirement)
      curr_state = $("#" + from.replace(form_type+"_"+dcd,state_var))[0].checked
      from_date = new Date($("#" + from).val())
    }
    else {
      from_date = new Date(value)
      to = parsleyInstance.$element[0].id.replace(requirement.replace('to', 'from'),requirement)
      curr_state = $("#" + to.replace(form_type+"_"+dcd,state_var))[0].checked
      to_date =  new Date($("#" + to).val())
    }

    if(curr_state == true){
      return true
    }
    return (from_date<to_date) ? true : false
  },
  requirementType: 'string',
  messages: {
    en: 'From date should be less than To date',
  }
});

$(document).ready(function() {
  var d = new Date();
    var todayDate = '' + (d.getMonth() + 1) + '/' + d.getDate() + '/' + d.getFullYear();

    function dateclass(el) {
      el.daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        maxDate:todayDate,
        autoUpdateInput: false,
        locale: {
          cancelLabel: 'Clear'
        }
      }, function(chosen_date) {
        el.val(chosen_date.format('YYYY-MM-DD'));
      });
    }

    $('.study_from, .work_from, .work_to, .study_to').each(function(){
      $(this).attr("readonly", "readonly")
      dateclass($(this));
    });

    $('#draft_form').click(function() {
      $('#linkedin-draft-form').parsley().on('field:validated', function() {
        var ok = $('.parsley-error').length === 0;
      })
      .on('#linkedin-draft-form:submit', function() {
        return false; // Don't submit form for this demo
      });
    });
    
    function updateElementIndex(el, prefix, ndx) {
      var id_regex = new RegExp('(' + prefix + '-\\d+-)');
      var replacement = prefix + '-' + ndx + '-';
      if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,replacement));
      if (el.id) el.id = el.id.replace(id_regex, replacement);
      if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function orgDeleteForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount > 1) {
      // Delete the item/form
        $(btn).parents('.org-add').remove();
        var forms = $('.org-add'); // Get all the forms
        // Update the total number of forms (1 less than before)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        var i = 0;
        // Go through the forms and set their indices, names and IDs
        for (formCount = forms.length; i < formCount; i++) {
          $(forms.get(i)).children().children().each(function() {
            updateElementIndex(this, prefix, i);
          });
        }
      } // End if
      else {
        alert("You have to enter at least one form!");
      }
      return false;
    }

    function eduDeleteForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount > 1) {
        // Delete the item/form
        $(btn).parents('.edu-add').remove();
        var forms = $('.edu-add'); // Get all the forms
        // Update the total number of forms (1 less than before)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        var i = 0;
        // Go through the forms and set their indices, names and IDs
        for (formCount = forms.length; i < formCount; i++) {
          $(forms.get(i)).children().children().each(function() {
            updateElementIndex(this, prefix, i);
          });
        }
      } // End if
      else {
        alert("You have to enter at least one form!");
      }
      return false;
    }

    function orgAddForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      var row = $('.org-add:first').clone(false).get(0);
      $(row).removeAttr('id').insertAfter($('.org-add:last')).children('.hidden').removeClass('hidden');

      $(row).children().not(':last').children().each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
        $(this).prop('checked', false);
        $(this).prop('disabled', false);
        $(this).removeClass("work_from");
        $(this).removeClass("work_to");
      });

      $(row).find('.org-delete').click(function() {
        orgDeleteForm(this, prefix);
      });

      $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);

      $('#id_'+prefix+'-' + formCount + '-work_from').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        autoUpdateInput: false,
        // startDate:'01/01/1960',
        maxDate:todayDate,
        // locale:{format: 'YYYY-MM-DD'}
      }, function(chosen_date) {
        $('#id_'+prefix+'-' + formCount + '-work_from').val(chosen_date.format('YYYY-MM-DD'));
      });

      $('#id_'+prefix+'-' + formCount + '-work_to').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        autoUpdateInput: false,
        // startDate:'01/01/1960',
        maxDate:todayDate,
        // locale:{format: 'YYYY-MM-DD'}
      }, function(chosen_date) {
        $('#id_'+prefix+'-' + formCount + '-work_to').val(chosen_date.format('YYYY-MM-DD'));
      });

      return false;
    }

    function eduAddForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount < 10) {
        var row = $(".edu-add:first").clone(false).get(0);
        // Insert it after the last form
        $(row).removeAttr('id').hide().insertAfter(".edu-add:last").slideDown(300);
        // Remove the bits we don't want in the new row/form
        // e.g. error messages
        $(".errorlist", row).remove();
        $(row).children().removeClass('error');
        $(row).children().children().each(function() {
          updateElementIndex(this, prefix, formCount);
          $(this).val('');
          $(this).attr('checked', false);
          $(this).attr("disabled", false);
          $(this).removeClass("study_from");
          $(this).removeClass("study_to");
        });
        // Add an event handler for the delete item/form link 
        $(row).find('.edu-delete').click(function() {
          return eduDeleteForm(this, prefix);
        });
        // Update the total form count
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);

        $('#id_'+prefix+'-' + formCount + '-study_from').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true,
          autoUpdateInput: false,
          // startDate:'01/01/1960',
          maxDate:todayDate,
          // locale:{format: 'YYYY-MM-DD'}
        }, function(chosen_date) {
          $('#id_'+prefix+'-' + formCount + '-study_from').val(chosen_date.format('YYYY-MM-DD'));
        });

        $('#id_'+prefix+'-' + formCount + '-study_to').daterangepicker({
          singleDatePicker: true,
          showDropdowns: true,
          autoUpdateInput: false,
          // startDate:'01/01/1960',
          maxDate:todayDate,
          // locale:{format: 'YYYY-MM-DD'}
        }, function(chosen_date) {
          $('#id_'+prefix+'-' + formCount + '-study_to').val(chosen_date.format('YYYY-MM-DD'));
        });
      } // End if
      else {
        alert("Sorry, you can only enter a maximum of ten items.");
      }
      return false;
    }
  // Register the click event handlers
    $("#org-add").click(function() {
      return orgAddForm(this, 'from_organization');
    });

    $("#edu-add").click(function() {
      return eduAddForm(this, 'from_education');
    });

    $(".org-delete").click(function() {
      return orgDeleteForm(this, 'from_organization');
    });

    $(".edu-delete").click(function() {
      return eduDeleteForm(this, 'from_education');
    });
    $('.current_org').click(function() {
      $('.work_to').attr('disabled', this.checked)
       $('.work_to').prop('required',false);
    });

    $('.current_edu').click(function() {
      $('.study_to').attr('disabled', this.checked)
       $('.study_to').prop('required',false);
    });


});