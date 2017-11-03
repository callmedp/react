$(document).ready(function() {
    $('#counselling-submit').click(function() {
        var element = 'submit-error';
        $("#dashboard_counselling_form").validate({
                submitHandler: function(form) {
                form.submit();
            },
            rules: {
                q1:{ required:true},
                q2: { required:true},
                q3:{ required:true},
                q4: { required:true},
                q5:{ required:true}        
            },
            messages:{
                q1:{ required:"This field is required"},
                q2:{ required:"This field is required"},
                q3:{ required:"This field is required"},
                q4:{ required:"This field is required"},
                q5:{ required:"This field is required"}   
            },
            errorPlacement: function(error, element) {
                element.siblings(".submit-error").text('This field is required');
            }
        });
    });
});