$(function(){
	var arr = []; 
	arr["qualification"] = ["Post Graduation", "Graduation", "Intermediate", "Matriculation"];
	arr["months"] = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
	arr["year"] = [];
	for(var yr = 1960; yr < 2017; yr++){
		arr["year"].push(yr);
	}
	arr["yrs"] = [];
	for(var yrs = 0; yrs < 12; yrs++){
		arr["yrs"].push(yrs + " years");
	}

	var _input = function(value, classValue){
		return '<input class="' + classValue + '" type="text" value="' + value + '"/>';
	}
	var _input2 = function(value1, value2){
		var value2 = typeof value2 != "string" ? "" : value2;
		var input2 = _input(value1, "pro-input2");
			input2 += _input(value2, "pro-input2");
		return  input2;
	}
	var _inputMobile = function(value1, value2){
		var mobinput = _input(value1, "pro-mob");
			mobinput += _input(value2, "pro-input2");
		return mobinput;
	}
	var _inputSelect = function(value1, value2, array){
		var value2 = typeof value2 != "string" ? "" : value2;
		var input2 = _input(value1,"pro-input2");
			// input2 += _select(value2, array, "pro-select2");
			input2 += '<a href="#" class="removeElement">Remove</a>';
		return  input2;
	}
	var _select = function(value, array, classValue){  
		var s = '<select class="' + classValue + '">';
			for(var i = 0; i < array.length; i++){
				if(value == array[i]){
					s += "<option selected>" + array[i] + "</option>";
				}
				else{
					s += "<option>" + array[i] + "</option>";
				}
			}
			s += "</select>"; 
		return s;
	}
	// Resume edit funciton 
	$.fn.resumeEdit = function(){
		return this.each(function(){
			var _type = $(this).data("role");
			switch(_type){
				case "input": 
					var _val = $(this).text();
					$(this).html(_input(_val, "pro-input"));
					break;
				case "input2":
					var _val = $(this).text();
					_val = _val.split(" ");
					if("yrmnth" == $(this).data("type")){
						$(this).html(_input2(_val[0] + _val[1], _val[2] + _val[3]));
					}else{
						$(this).html(_input2(_val[0], _val[1]));
					}
					break;
				case "select":
					var _val = $(this).text();
					var _array = $(this).data("type");
					$(this).html(_select(_val, arr[_array], "pro-select"));
					break;
				case "inputSelect": 
					var _val1 = $(this).children("div").eq(0).text();
					var _val2 = $(this).children("div").eq(1).text();
					var _array = $(this).data("type");
					$(this).html(_inputSelect($.trim(_val1), $.trim(_val2), arr[_array]))
							.removeClass("skill-box").addClass("col-sm-9 col-md-9 mb-10")
						.parent().removeClass("block-inline").addClass("row mt10");
					break;
				case "mobile":
					var _val = $(this).text().split("-");
					$(this).html(_inputMobile(_val[0], _val[1]));
					break;
			}


		});
	}
});

$(document).ready(function(){


	/*$('.tabs_links li').on("click", function (e) {
		e.preventDefault();
		$(".tabs_links li").removeClass("active");
		$(this).addClass("active");
         $('html, body').animate({
             scrollTop: $('[data-id='+ $(this).data("target") +']').offset().top - 100
         }, 'slow');
    });*/





	$(document).on("click", "[data-role=button]", function(){
		var	_parent = $(this).closest("div");
		_parent.find("[data-editable]").resumeEdit();
		$(this).css("display", "none").attr("disabled","disabled");
		_parent.find(".save-event").css("display", "");
		if($(this).prev().text() == "Skills"){
			var _firstSkill = _parent.find("[data-editable]").eq(0);
			_firstSkill.parent().prepend('<div class="col-sm-3 col-md-3">Key Skills/Experience</div>');
			_firstSkill.removeClass("col-sm-push-3 col-md-push-3");
			_firstSkill.find("a").remove();
		}
	});

	$(document).on("click", ".removeElement", function(e){
		e.preventDefault();
		$(this).closest(".row").remove();
	});

	$(document).on("click", ".addElement", function(e){
		e.preventDefault();
		var inputsRow = '<div class="row mt10">' +
						'<div class="col-sm-9 col-md-9 col-sm-push-3 col-md-push-3 mb-10" data-role="inputSelect" data-editable="" data-type="yrs">' +
							'<input class="pro-input2" value="" type="text">' +
							// '<select class="pro-select2"><option>0 years</option><option>1 years</option><option>2 years</option><option>3 years</option><option>4 years</option><option>5 years</option><option>6 years</option><option>7 years</option><option>8 years</option><option>9 years</option><option>10 years</option><option>11 years</option></select>' + 
							'<a href="#" class="removeElement">Remove</a>' +
						'</div>' +
                        '</div>';
		$(this).closest(".row").before(inputsRow);
	});
	// resume update
	$(document).on("click", ".resume-close", function(e){
		e.preventDefault();
		$(this).closest(".alert-resume").html("")
			.html('<a href="#" class="add-resume">Add Resume</a>' + '<input class="hidden" type="file" id="resume" />')
			.addClass("text-center");
	});

	$(document).on("click", ".add-resume", function(e){
		e.preventDefault();
		$(this).next("input").click();
	});

	$(document).on("change", "#resume", function(){
		$(".alert-resume")
			.html('<a href="#">' + $(this).val() + '</a><div class="pull-right resume-close"><a href="#">X</a></div>')
			.removeClass("text-center");
	});
	
	$('input[type="checkbox"]').click(function(){
		if($(this).is(":checked")){
		  $(".endyear").hide();
		  $(".endmonth").hide();
		}
		else if($(this).is(":not(:checked)")){
		  $(".endyear").show();
		  $(".endmonth").show();
		}
	});

});