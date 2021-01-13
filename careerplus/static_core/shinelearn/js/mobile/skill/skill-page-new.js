/*
Following Funtions are used in skill page desktop
    1. loadProduct => load courses or assesment in skill page
    2. needHelpFormSubmit => helper function to submit need help form response
    3. openMoreFAQ => to show faq is cound is more than 2
    4. stickyNavbarActiveScroll => used to make sticky navbar active in its elements while scrolling
    5. changeTab => Change tab between courses and assessments.
    6. needHelpFormValidation => validate the need help form using jquery validate
    7. indiaMobileValidator =>  To add a new validation rules of indian mobile no in jquery validate
    8. lettersOnlyValidator =>  To add a new validation rules of letters only in jquery validate
    9. gaEventFunc => gaEvent function for enquiry form
    10. needHelpFormDOMEffect =>  need help form button ANimated effect

*/


//global variable used in this js file
let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5  //get only 5 products in every api resonse to load product
let categoryId = null  // for load product fucntion
let timeoutID = null  // store the setimeout id



$(document).ready(()=>{
    //categoryid and heading form couse list attributes
    categoryId = $('#tab-bar').attr('categoryId');

    $('.scrollTo').click(function(e){
        timeoutID ? clearTimeout(timeoutID):''
        stickyNavbarActiveScroll(false) //false argument is to stop active scroll
        var height = $('.sticky-header').height() + 10;
        $('html, body').animate({
            scrollTop: $( $(this).attr('href') ).offset().top - height
        }, 500);
    
        e.stopPropagation();
        $(".active").removeClass("active");
        $(this).addClass("active");
        timeoutID = setTimeout(() => {
            stickyNavbarActiveScroll(true) //true argument is to start active scroll
        }, 1500);   
        return false;
    });

    stickyNavbarActiveScroll(true)
    indiaMobileValidator()
    lettersOnlyValidator()
    needHelpFormValidation()
    needHelpFormDOMEffect()

    $(".main-banner__slider").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: true
	});

	$(".popular-courses__slides").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		infinite: true
	});

	$(".learner-stories__slider").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		infinite: true
    });  
    
})

//load courses or assessment 
//arg1 : el => used to remove the button when more products cannot be loaded
//arg2 : type => deciding whether course or product to be loaded
//This function sends a get request to get products and append them to dom
const loadProduct = (el,type) => {
    const pTFInclude = type==='course'?false:true
    const pageNo = type==='course'?coursePageNo:assessmentPageNo
    const productTypeId = type==='course'?'#tab-1':'#tab-2'
    const loaderDiv = $(el).parent().find('div')
    $(el).hide()
    loaderDiv.removeClass('hide')

    $.get(`api/v1/load-more/`,
    {
        "page": pageNo, "page_size": pageSize, "pCtg" : categoryId, 
        "pTF" : 16 ,"pTF_include" : pTFInclude,  
        "fl" : "name,pCert,pURL,pImg,pNm,pNJ,pHd,pStar,pARx,pPin,pPfin,pPvn,discount,pAsft,pTg"
    }
    ,(data)=>{
        let products = data.results
        if (products)
            type==='course'?coursePageNo+=1:assessmentPageNo+=1
        
        for (key in products){
            $(productTypeId).find('ul').append(`
                <li class="d-flex row">
                    <span class="skill-tabs--image">
                        <img aria-label="${products[key].pNm}" src="${products[key].pImg}" alt="${products[key].pNm}">
                    </span>

                    <div class="skill-tabs__content">
                        ${products[key].pTg ==1 ?
                            `<div class="skill-tabs__content--tag skill-tabs__content--bestseller">Bestseller</div>`:
                        products[key].pTg ==  2?
                            `<div class="skill-tabs__content--tag skill-tabs__content--new">Newly Added</div>`:''
                        }
                        <a class="d-block pt-5" href="${products[key].pURL}"><strong>${products[key].pNm}</strong></a>
                        <div class="ratingView mt-10">
                            <span class="rating" data-rating="${ Math.round((products[key].pARx)*100)/100 }"></span> 
                            ${ Math.round((products[key].pARx)*100)/100 }/5
                        </div>
                        ${products[key].pStM ? 
                            `<div class="skill-tabs__content--mode">
                                Mode 
                                ${products[key].pStM.map((item)=>(
                                    `<span>${modeChoices[item]}</span>`
                                )).join(' ')}
                            </div>`:''
                        }
                      
                        ${products[key].pPvn ?
                            `<p class="skill-tabs__content--provider fs-11"><small class="mr-5">Provider</small>${products[key].pPvn}</p>`:''
                        }
                        <p class="skill-tabs__content--price"><strong>Rs. ${ Math.round((products[key].pPin)*100)/100 }/- </strong></p>
                    </div>
                </li>
            `)
        }

        loaderDiv.addClass('hide');
        !data.next ? $(el).parent().hide():$(el).show();

    })
}
// submit need help form
const needHelpFormSubmit = (formData,lsource) => {
    $.post(`/lead/lead-management/`,formData,(data)=>{
        lsource[0] ? gaEventFunc(lsource[0].value,'success'):''
        Toast.fire({
            type: 'success',
            title: 'Query Form submitted'
        })
        $("#callUsForm").find("input[type=text]").val("");
	    showHideElement(false,'enquire')
    }).fail(()=>{
        lsource[0] ? gaEventFunc(lsource[0].value,'failure'):''
        Toast.fire({
            type: 'error',
            title: 'Something went wrong'
        })
    })

}


//Open More FAQ
const openMoreFAQ = () =>{    
    $('.css-accordion').children('.css-accordion--tab').each(function(){
        $(this).removeClass('hide')
    })
    $('#more-faq').addClass('hide')
}


//Funtion used to set activate of sticky nav while scrolling
const stickyNavbarActiveScroll = (startStickyActiveScroll) => {
    var topMenu = $("#sticky-header"),
    topMenuHeight = topMenu.outerHeight()+15,
    // All list items
    menuItems = topMenu.find("a"),
    // Anchors corresponding to menu items
    scrollItems = menuItems.map(function(){
      var item = $($(this).attr("href"));
      if (item.length) { return item; }
    });

    var showStickyNavbarHandler = () =>{
        $(this).scrollTop() > 10 ?  $('.sticky-header').addClass('fixed'): $('.sticky-header').removeClass('fixed');
    }

    var scrollHandler = () => {
        let fromTop = $(this).scrollTop()+topMenuHeight;

        // Get id of current scroll item
        let cur = scrollItems.map(function(){
            if ($(this).offset().top < fromTop)
            return this;
        });
        if (cur.length > 0){
            // Get the id of the current element
            cur = cur[cur.length-1];
            let id = cur && cur.length ? cur[0].id : "";
             // Set/remove active class
            menuItems.removeClass("active");
            let activeItem = menuItems.filter(`[href="#${id}"]`)
            activeItem.addClass("active");


            var activeWidth = activeItem.width() / 2; // get active width center

            var pos = activeItem.position().left + activeWidth; //get left position of active li + center position
            var elpos = $('.scrolling-wrapper-flexbox').scrollLeft(); // get current scroll position
            var elW = $('.scrolling-wrapper-flexbox').width(); //get div width
            pos = pos + elpos - elW / 2; // for center position if you want adjust then change this

            $('.scrolling-wrapper-flexbox').animate({
                scrollLeft: pos
            }, 0);
        }

    }

     // Bind to scroll
     startStickyActiveScroll ? $(window).on('scroll',scrollHandler) : $(window).off('scroll')
     $(window).on('scroll',showStickyNavbarHandler)
}

//change tab between courses and assessment in skill page mobile
const changeTab = (setTabId,removeTabId) => {
    $(`#${setTabId}`).addClass('current')
    $(`#${removeTabId}`).removeClass('current')
    $(`#${setTabId}-text`).addClass('current')
    $(`#${removeTabId}-text`).removeClass('current')
}

// funtion to set rukes and validate need help form
const needHelpFormValidation = () => {
    var callUsForm = $("#callUsForm");
    callUsForm.validate({
        errorClass:'error--mgs',
        errorElement:'span',
        rules: {
            name: {
                required: true,
                lettersonly: true,
                maxlength: 100
            },
            email: {
                required: true,
                email:true,
                maxlength: 100
            },
            number: {
                required: true,
                digits: true,
                indiaMobile: true,
                minlength: 4,
                maxlength: 15,
            },

        },
        messages: {
            name: {
                required: "Required",
                lettersonly: 'Letters Only',
                maxlength: "Max length 100"
            },
            email: {
                required: "Required",
                email:'Not Email',
                maxlength: "Max length 100"
            },
            number: {
                required: "Required",
                digits: "Only Digits",
                indiaMobile: "10 digits only",
                minlength: "Add atleast 4 digits",
                maxlength: "Add less than 16 digits",

            },
        },
        highlight: function(element, errorClass) {
            $(element).parent().addClass('error') 
        },
        unhighlight: function(element, errorClass) {
            $(element).parent().removeClass('error') 
        },
        // errorPlacement: errorPlacement,
        submitHandler: function(form){
            lsource =$(form).serializeArray().filter((el)=>{
                if(el.name === 'lsource')
                    return el;
            })
            var formData = $(form).serialize();
            needHelpFormSubmit(formData,lsource)
        }
    });
}

// fucntion to add a new validation rules of indian mobile no in jquery validate
const indiaMobileValidator = () => {
    $.validator.addMethod("indiaMobile", function(value) {
        var country_code = $('#country-code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });
}

// fucntion to add a new validation rules of letters only in jquery validate
const lettersOnlyValidator = () => {
    $.validator.addMethod("lettersonly", function(value, element) {
        return this.optional(element) || /^[a-z," "]+$/i.test(value);
    }); 
}

function gaEvent(event_cat,event_lab,event_action){
    ga('send', 'event', event_cat, event_action, event_lab);
    }

//gaEventFucnt for enquiry form
const gaEventFunc = (typeOfProduct,status) =>{
    var event_cat='Form Interactions';

    var type = "" ;
    if(typeOfProduct == "1"){
        type= 'Skill Course Enquiry';
    }
    else{
        type= 'Skill Service Enquiry';
    }
    gaEvent(event_cat,status,type);
}

// need help form button ANimated effect
const needHelpFormDOMEffect = () => {
    $(".input-effect input").blur(function(){
        $(this).val() !== "" ? $(this).addClass("has-content"):$(this).removeClass("has-content");
    })
}
        


