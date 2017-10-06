$(document).ready(function(){

    $("#id_search_location").multipleSelect({
        width: 100,
        filter: true,
        selectAll: true,
        placeholder: "Location",
        allSelected: "All Location",
        selectAllText: "All Location",
        selectAllDelimiter: [],
        onClick: function(view){
            selected =  $("#id_search_location").multipleSelect("getSelects");
            if (selected.length >= 10){
                $("input[data-name=selectItemlocation]:unchecked").prop('disabled', true);
            }else{
                $("input[data-name=selectItemlocation]").prop('disabled', false);
            }
        }
    });

    $("input[data-name=selectAlllocation]").on("change", function(){
        if($("input[data-name=selectAlllocation]").is(":checked")){
            $("input[data-name=selectItemlocation]").prop('disabled', true);
        }else{
            $("input[data-name=selectItemlocation]").prop('disabled', false);
        }
    });
});

function updateQueryParams(param, value, regex){
    if(document.location.search.length > 0){
        if(document.location.search.indexOf(param) > 0){
            var paramvalue = param + '=' + value;
            var searchparam = document.location.search.replace(regex, paramvalue);
            document.location.href = searchparam;
        }else{
            var appendparam = '&' + param + '=' + value;
            document.location.href += appendparam;
        }
    }else{
        var queryparam = '?' + param + '=' + value;
        document.location.href = queryparam;
    }
}

function onClickRoundOneSearch(){
    var keyword = $.trim($("input[name=keyword]").val());
    var city_list = $("#id_search_location").multipleSelect("getSelects");
    if(city_list.length > 10 || city_list.length < 1){
        city_list = ["all"];
    }
    if(keyword.length < 1){
        keyword = "all";
    }
    city = city_list.join(" ");
    window.location.href = "/partner/roundone/" + $.trim(keyword.replace(/\W+/g,' ')).replace(/\W+/g,'-').toLowerCase() + "-jobs-in-" + $.trim(city.replace(/\W+/g, " ")).replace(/\W+/g, "-").toLowerCase() + "/?loc=" + city_list;
}

$("#roundone_search").bind("keypress", function(e){
    if(e.keyCode == 13){
        onClickRoundOneSearch();
    }
});

function send_xhr (ajaxurl, idx) {
    showLoader();
    $.ajax({
        url: ajaxurl,
        type: "post",
        data: $("#id_"+idx).serialize(),
        success: function(response){
            result = JSON.parse(response);

            if(result.status){
                if(result.redirect && result.redirect_url.length > 0) 
                {
                    window.location.href = result.redirect_url;
                }
                else if(result.response)
                {
                    hideLoader();
                    // $("#api_rsp").modal('show');
                    showSuccessModal(result.message, "Ok");
                }
            }
            else
            {
                showErrorModal(result.message, "Ok", "Cancel");
            }
        },
        failure: function(response){
            $('.savejob_js').removeClass('disabled');
        },
        complete: function(response){
            $('.savejob_js').removeClass('disabled');
            hideLoader();
        }
    });
}

function onClickSaveJob(eleme, idx){
    if ($(eleme).hasClass('disabled')) return;
    $('.savejob_js').addClass('disabled');
    ajaxurl = $("input[name=roundone-save-job]").val();
    send_xhr(ajaxurl, idx);
}

$("#id_search_sort").off().on("change", function(){
    var param="sort";
    var re = param +'=\\d+';
    var regex = new RegExp(re, "g");
    updateQueryParams(param, this.value, regex);
});

function onClickLoadResult(page_no){
    var param = "page";
    var re = param +'=\\d+';
    var regex = new RegExp(re, "g");
    updateQueryParams(param, page_no, regex);
}

$("#id_applyfilter").off().on("click", function(){
    var company = [];
    var param = "company";
    var re = param +'=(\\d+,?)+\\d+';
    var regex = new RegExp(re, "g");
    $("input[name=filterbyCompany]:checked").each(function(){
        company.push($(this).val());
    });
    if (company.length > 0){
        company_list = company.join(",");
        updateQueryParams(param, company_list, regex);
    }else{
        // resetting filter
        if(document.location.search.length > 0){
            var search_arr = document.location.search.split("?");
            if (search_arr.length > 0){
                search_string = search_arr[1];
                if(search_string.length > 0){
                    var re = '\\&?' + param +'=(\\d+,?)+\\d+';
                    var regex = new RegExp(re, "g");
                    updated_href = search_string.replace(regex, "")
                    document.location.href = "?" + updated_href;
                }
            }
        }
    }
});

function onclickBuyNow(obj) {
  var data, _this;
  _this = $(obj);
  if ($(obj).hasClass('disabled')) {
    return false;
  }
  data = _this.data();
  _this.addClass('disabled');
   _gaq.push(['resume._trackEvent','Cart','add_from_compare']);
  $.post('/ajax/cart/add/', data, function(response) {
    var message;
    _this.removeClass('disabled');
    if (response.status) {
      // update_cart(response);
      $('#cart_btn').trigger('click');
    }
    if (response.message) {
      message = response.message;
      return showErrorModal(message, "Ok", "Cancel");
    }
  }, 'json');
  return false;
}