var showChar = 280;  // How many characters are shown by default
var ellipsestext = "...";
var moretext = " know more";
var lesstext = " know less";

function showMoreLess() {
  // Configure/customize these variables.

  $('.more').each(function () {
    var content = $(this).html();

    if (content.length > showChar) {

      var c = content.substr(0, showChar);
      var h = content.substr(showChar, content.length - showChar);
      var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="#" class="morelink" style="display:inline-block;">' + moretext + '</a></span>';


      $(this).html(html);
    }

  });

};

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$.validator.addMethod("custom_review",
  function (value, element) {
    if ($('#id_review').val().trim()) {
      return true;
    }
    return false;
  });
$("#feedback-form").validate({
  rules: {
    rating: {
      required: true,
    },
    review: {
      maxlength: 1500,
    },
    title: {
      required: true,
    }
  },
  messages: {
    average_rating: {
      required: "rating is required."
    },
    review: {
      maxlength: "length should not be greater than 1500 characters.",
    },
    title: {
      maxlength: "length should not be greater than 20 characters."
    }
  },
  errorPlacement: function (error, element) {
    $(element).siblings('small').find('.error').html(error.text());
  },
  submitHandler: function (form) {
    return false;
  },

});
function feedback_submit(formData) {

  var flag = $('#feedback-form').valid();
  var rating_flag = false;
  $('input[name="rating"]').each(function () {
    if ($(this).prop('checked') == true) {
      rating_flag = true;
    }
  });
  if (!rating_flag) {
    $('#rating-error').text('rating is mandatory');
  }
  if (flag && rating_flag) {
    request_to_submit_feedback(formData)
  }

}

function request_to_submit_feedback(formData) {
  $.ajax({
    url: '/shop/reviews/product/create/',
    type: 'POST',
    data: formData,
    dataType: 'json',
    async: false,
    timeout: 30000,
    success: function (json) {
      if (json.success) {
        alert(json.display_message);
        window.location.reload();
      }
      else if (json.display_message) {
        alert(json.display_message)
        refreshErrors(json)
      }
      else {
        refreshErrors(json)
      }
    },
    error: function (xhr, ajaxOptions, thrownError) {
      alert("Something went wrong, try again later");
    }
  });
}

function refreshErrors(json) {
  var keys = ['review', 'title', 'rating']
  keys.forEach(function (element) {
    if (json[element]) {
      $('#' + element + '-error').text(json[element]);
    }
    else {
      $('#' + element + '-error').text('');
    }
  });
}

function submit_feedback_form(is_logged_in) {
  if (is_logged_in == 'True') {
    var formData = $('#feedback-form').serialize();
    feedback_submit(formData);
  }
  else {
    var flag = $('#feedback-form').valid();
    if (flag) {
      $('#login-modal').modal('show');
    }
  }
}

function update_feedback_form(product_pk) {
  var formData = $('#feedback-form').serialize();
  $.ajax({
    url: '/shop/reviews/' + product_pk + '/edit/',
    type: 'POST',
    data: formData,
    dataType: 'json',
    success: function (json) {
      if (json.success) {
        alert(json.display_message);
        window.location.reload();
      }
      else if (json.display_message) {
        alert(json.display_message)
        refreshErrors(json)
      }
      else {
        refreshErrors(json)
      }
    },
    error: function (xhr, ajaxOptions, thrownError) {
      alert("Something went wrong, try again later");
    }
  });
}
$(document).on('click', '[name="rating"]', function () {
  var flavour = $('[name="flavour"]').val();
  console.log(flavour);
  if (flavour == 'mobile') {
    var rating_val = $(this).attr('value');
    $('#selected-rating').text(rating_val);
  }
  else {
    var html = $(this).attr('value') + '<small>/5</small>';
    $('#selected-rating').html(html);
  }
  $('#rating-error').text('');

});


function submitReviewFromLocalStorage() {
  formData = localStorage.getItem("formData");
  if (formData) {
    request_to_submit_feedback(formData);
    localStorage.removeItem("formData");
  }
  else {
    localStorage.removeItem("formData");
  }
}

function saveReviewFormDataToLocalStorage() {
  var formData = $('#feedback-form').serialize();
  if (formData) {
    localStorage.setItem('formData', formData);
  }
}

function reviewLinkedInLogin() {

  saveReviewFormDataToLocalStorage()
  window.location.href = '/user/linkedin/code/?next=' + window.location.href
}
submitReviewFromLocalStorage()

$(document).ready(function () {

  // $(window).on('load',function(){
  //   $('#login-model').modal('show');
  // });

  // $(document).on("click", "#login-now-button", function() {
  //   $('#login-model').modal('show');
  // });

  $('#login-button').click(function () {
    flag = $("#login_form").valid();
    if (flag) {
      var formData = $("#login_form").serialize();
      $('#login-button').prop('disabled', true);
      $.ajax({
        url: "/article/login-to-comment/",
        type: "POST",
        data: formData,
        async: false,
        timeout: 30000,
        success: function (data, textStatus, jqXHR) {

          if (data.response == 'login_user') {
            var formData = $('#feedback-form').serialize();
            feedback_submit(formData)
            window.location.reload();
          }
          else if (data.response == 'error_pass') {
            var error_message = data.error_message;
            $('#non-field-error').text(error_message)
          }
          else if (data.response == 'form_validation_error') {
            $('#non-field-error').text('Please enter Valid Data')
          }
          $('#login-button').prop('disabled', false);
        },
        error: function (jqXHR, textStatus, errorThrown) {
          alert('Something went wrong. Try again later.');
          $('#login-button').prop('disabled', false);
        }
      });
    }
  });


  var processing = false;

  function LoadMoreProductReview(pv_id) {
    if (processing) {
      return false;
    }
    else {
      if (pv_id) {
        try {
          let page, elem;
          elem = document.getElementById("id_review_page");
          try {
            elem.value = parseInt(elem.value) + 1;
          } catch (_error) {
            i = _error;
            elem.value = 2;
          }
          page = document.getElementById("id_review_page").value;
          processing = true;

          $.ajax({
            url: '/shop/reviews/' + encodeURIComponent(pv_id) + '/?pg=' + encodeURIComponent(page),
            dataType: 'html',
            success: function (html) {
              $('#loadmorereviewbtn').remove();

              $('#id_review_list').append(html);

            },
            complete: function (response) {
              return processing = false;
            },
            error: function (xhr, ajaxOptions, thrownError) {
              alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);
            }
          });
        }
        catch (e) {
          alert("Invalid Page");
        }
      }
    }
  };


  $(document).on("click", ".other-product", function () {
    var data_pk = $(this).attr('data-id');
    var main_pk = $(this).attr('main-id');
    data = "?main_pk=" + main_pk + "&obj_pk=" + data_pk;
    $.ajax({
      url: "/shop/product/content-by-ajax/" + data,
      type: "GET",
      dataType: "json",
      success: function (data) {

        skill = data.skills;
        if (data.status == 1) {
          currentUrl = top.window.location.pathname;
          $("#id-detail-body").empty();
          $('#id-detail-body').html(data.detail_content);
          if (typeof (history.pushState) != "undefined") {

            var obj = { Title: data.title, Url: data.url };
            history.pushState(obj, obj.Title, obj.Url);
            document.title = data.title;
          }
          checkedInitialRequired();
          updateCartPrice();
          showMoreLess();
          $('.cls_scroller').scrollerdiv();
          $('.cls_sticky_scroller').productdetailAnimations();
          activeOnScroll.init({ className: '.cls_scroll_tab' });
          ajax_call(authen, data_pk);
        }
      },
      failure: function (response) {
        ajax_call(authen, data_pk);

      }
    });


  });


  $(document).on("click", ".review-load-more", function () {

    LoadMoreProductReview($(this).attr('data-product'));
  });


  $.validator.addMethod("indiaMobile", function (value, element) {
    var country_code = $("input[name=country_code]").val(); //$('#call_back_country_code-id').val();
    if (country_code == '91') {
      return value.length == 10;
    }
    return true;
  });



  $(document).on('click', '#id_callback', function () {
    $('#callback_form').validate({
      rules: {
        name: {
          required: true,
          maxlength: 80,
        },
        number: {
          required: true,
          number: true,
          indiaMobile: true,
          // minlength: 4,
          maxlength: 10
        },
        msg: {
          required: true,
          maxlength: 500,
        },
        email: {
          required: true,
          maxlength: 100,
          email: true,
        }
      },
      messages: {
        name: {
          required: "Name is Mandatory.",
          maxlength: "Maximum 80 characters.",
        },
        email: {
          required: "Email is Mandatory.",
          maxlength: "Please enter at most 100 characters.",
          email: "Please enter valid email"
        },
        number: {
          required: "Mobile Number is Mandatory",
          number: "Enter only number",
          indiaMobile: "Please enter 10 digits only",
          maxlength: "Please enter 10 digits",
          // minlength: "Please enter atleast 4 digits"
        },
      },
      highlight: function (element, errorClass) {
        $(element).closest('.form-group').addClass('error');
      },
      unhighlight: function (element, errorClass) {
        $(element).closest('.form-group').removeClass('error');
        $(element).siblings('.error-txt').html('');
      },
      errorPlacement: function (error, element) {
        $(element).siblings('.error-txt').html(error.text());
      },
      ignore: '',
      submitHandler: function (form) {
        // ga code
        var path = window.location.pathname,
          action = '';
        if (path.indexOf('/course/') > -1) {
          action = 'Course Enquiry';
        } else if (path.indexOf('/services/') > -1) {
          action = 'Service Enquiry';
        }
        MyGA.SendEvent('QueryForm', 'Form Interactions', action, 'success');
        //form.submit();
        var formData = $(form).serialize();
        $.ajax({
          url: "/lead/lead-management/",
          type: "POST",
          data: formData,
          success: function (data, textStatus, jqXHR) {
            alert('Your Query Submitted Successfully.');
            $("#detailpage").modal('toggle');
            form.reset();
          },
          error: function (jqXHR, textStatus, errorThrown) {
            alert('Oops Some error has occured. Kindly try again later.');
            $("#detailpage").modal('toggle');
            form.reset();
          }
        });
      }
    });

    var flag = $('#callback_form').valid();
    if (flag) {
      $('#callback_form').submit();
    }
  });

  // scroll effect;
  activeOnScroll.init({ className: '.cls_scroll_tab' });
});
$(document).ready(function () {
  showMoreLess();

  $(document).on('click', '.morelink', function (e) {
    if ($(this).hasClass("less")) {
      $(this).removeClass("less");
      $(this).html(moretext);
    } else {
      $(this).addClass("less");
      $(this).html(lesstext);
    }
    $(this).parent().prev().toggle();
    $(this).prev().toggle();
    return false;
  });

  // $('.about-tab a').click(function(){
  //   $('.about-tab a').removeClass('active');
  //   $(this).addClass('active');
  // });

  $(document).on('click', '.cls_scroll_tab', function (e) {
    e.preventDefault();
    e.stopPropagation();
    var navBarHeight = $('#id_nav').outerHeight() || 0;
    var stickyBarHeight = $(".cls_sticky_scroller").outerHeight() || 0;
    var target = $(e.target);
    if (target.hasClass('cls_tab_child')) {

      $('html,body').animate({ scrollTop: $('' + target.attr('href')).offset().top - target.outerHeight() - stickyBarHeight - navBarHeight }, 1000);
    }
  });

  $(document).on('click', '.cls_review', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $('#review-tab').trigger('click');
  });

  function getUrlVar(key) {
    var result = new RegExp(key + "=([^&]*)", "i").exec(window.location.search);
    return result && unescape(result[1]) || "";
  }
  var res = getUrlVar('query');
  if (res == 'True') {
    $('#detailpage').modal('show');
  }


  $(document).on('click', '#redeem_test', function (e) {
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')
    const prodId = $(this).attr('prod-id')
    const redeemOption = $(this).attr('redeem-option')
    createDirectOrder(prodId, redeemOption)
  })


});


function ajax_call(authen, prod_id) {
  if (skill != false) {
    $.ajax({
      url: "/api/v1/recommended-products/?skills=" + skill + "&product=" + prod_id + "&page_size=" + 6,
      type: "GET",
      success: function (data, textStatus, jqXHR) {
        var count = ((data.results).length);
        var i;
        if (count) {
          document.getElementById('heads').style.display = "block";
          var recom = "";
          if (authen) {
            recom += '<h2 class="detail-heading">Recommended products</h2>';
          }
          else {
            recom += '<h2 class="detail-heading">Related products</h2>';
          }
          recom += '<div class="row">' +
            '<ul class="listing">';

          for (i = 0; i < count; i++) {

            var first = '<li class="col-sm-6 col-md-4">' +
              '<a title="' + (data.results[i].pHd).substring(0, 40) + '"class="box-panel" href="' + data.results[i].pURL + '">' +
              '<div class="media">' +
              '<div class="media-body">' +
              '<h3 class="listing-heading">'
              + data.results[i].pHd + '</h3>'
              + '<div class="rating-review-box">';
            if (data.results[i].pRC) {

              for (star in data.results[i].pStar) {

                if (data.results[i].pStar[star] == "*") {
                  first = first + '<figure class="full-star"></figure>';
                }
                else if (data.results[i].pStar[star] == "+") {
                  first = first + '<figure class="half-star"></figure>';
                }
                else {
                  first = first + '<figure class="blank-star"></figure>';
                }

              }
              first = first + '<strong><small>' + (data.results[i].avg_rating) + '</small>/5</strong>'
            }
            else {
              first = first + '<strong>' + data.results[i].buy_count + '</strong> people bought'
            }
            var second = '<span class="jobs-available"><strong>' + data.results[i].no_jobs + '</strong> jobs available</span>' +
              '</div>' +
              '</div>' +
              '<div class="media-left">' +
              '<figure>' +
              '<img class="img-responsive" src="' + data.results[i].pImg + '" alt="' + data.results[i].pImg + '">' +
              '</figure>' +
              '</div>' +
              '</div>' +
              '</a>' +
              '</li>';
            recom = recom + first + second;
          }
          +'</ul>'
            + '</div>'
            + '</div>'
            + '</div>'
            + '</div>';


          document.getElementById('recommended_product').innerHTML = recom;
        }
        else {
          document.getElementById('recommended_product').innerHTML = "";
        }
      }
    });
  }
  else {
    document.getElementById('recommended_product').innerHTML = "";

  }
};


function createDirectOrder(productId, redeem_option) {

  $.ajax({
    url: '/api/v1/order/direct-order/',
    type: 'POST',
    data: { 'prod_id': productId, 'redeem_option': redeem_option },
    dataType: 'json',
    success: function (json) {
      if (json.status == 1) {
        window.location.href = json.redirectUrl;
      }
      else if (json.status == -1) {
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        alert(json.error_message);
      }

    },
    failure: function (response) {
      $('.overlay-background').hide()
      $('body').removeClass('body-noscroll')
      alert("Something went wrong, Please try again");

    },
    error: function (xhr, ajaxOptions, thrownError) {
      $('.overlay-background').hide()
      $('body').removeClass('body-noscroll')
      alert("Something went wrong, Please try again");
    }
  });

}
