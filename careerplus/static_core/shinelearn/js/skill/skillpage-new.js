/*
Following Funtions are used in skill page desktop
    1. loadProduct => load courses or assesment in skill page
    2. needHelpFormSubmit => helper function to submit need help form response
    3. openMoreFAQ => to show faq is cound is more than 2
    4. stickyNavbarActiveScroll => used to make sticky navbar active in its elements while scrolling
    5. needHelpFormValidation => validate the need help form using jquery validate
    6. indiaMobileValidator =>  To add a new validation rules of indian mobile no in jquery validate
    7. lettersOnlyValidator =>  To add a new validation rules of letters only in jquery validate
    8. gaEventFunc => gaEvent function for enquiry form

*/


//global variable used in this js file
let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5  //get only 5 products in every api resonse to load product
let categoryId = null  // for load product fucntion
let timeoutID = null  // store the setimeout id

/*  About section height from top (USE CASE => show sticky nav in skill page when this height reaches 
    This is set in document in ready before calling stickyNavbarActiveScroll function
*/
let aboutSectionPosTop = null 


$(document).ready(()=>{
    categoryId = $('#course-list').attr('categoryId');

    $('.sticky-nav .nav-link').click(function(){
        timeoutID ? clearTimeout(timeoutID):''
        stickyNavbarActiveScroll(false) //false argument is to stop active scroll
        $('.sticky-nav .nav-link').removeClass('active');
        $(this).addClass('active');
        timeoutID = setTimeout(() => {
            stickyNavbarActiveScroll(true) //true argument is to start active scroll
        }, 1500);

    })

    aboutSectionPosTop = $('#about').offset().top
    stickyNavbarActiveScroll(true) //true argument is to start active scroll
    needHelpFormValidation()
    lettersOnlyValidator()
    indiaMobileValidator()

})

//load courses or assessment 
//arg1 : el => used to remove the button when more products cannot be loaded
//arg2 : type => deciding whether course or product to be loaded
//This function sends a get request to get products and append them to dom
const loadProduct = (el,type) => {
    const pTFInclude = type==='course'?false:true
    const pageNo = type==='course'?coursePageNo:assessmentPageNo
    const productTypeId = type==='course'?'#course-list':'#assessment-list'
    const loaderDiv = $(el).parent().find('div')
    $(el).hide()
    loaderDiv.removeClass('d-none')

    $.get(`api/v1/load-more/`,
    {
        "page": pageNo, "page_size": pageSize, "pCtg" : categoryId, 
        "pTF" : 16 ,"pTF_include" : pTFInclude,  
        "fl" : "name,pCert,pURL,pImg,pNm,pNJ,pHd,pStar,pARx,pPin,pPfin,pPvn,discount,pAsft,pStM,pTg"
    }
    ,(data)=>{
        let products = data.results
        if (products)
            type==='course'?coursePageNo+=1:assessmentPageNo+=1
        
        for (key in products){
            $(productTypeId).append(`
                <li class="media listing__list">
                    <figure class="listing__image">
                        <img aria-label="${products[key].pNm}" class="img-fluid" src="${products[key].pImg}" alt="${products[key].pNm}">
                    </figure>
                    
                    <div class="media-body">
                    <h3><a href="${products[key].pURL}">${products[key].pNm}</a></h3>
                        <div class="rating">
                        ${products[key].pStar.map((rating)=>{
                            return rating==='*'?'<i class="b4-icon-star"></i>':rating==='+'?
                                    '<i class="b4-icon-star"></i>':'<i class="b4-icon-star-blank"></i>'
                        }).join('')}
                            
                        
                        <span class="rating__output">${ Math.round((products[key].pARx)*100)/100 }/5</span>
                        </div>

                        ${products[key].pStM ? 
                                    `<div class="mode mr-30">
                                        Mode 
                                        ${products[key].pStM.map((item)=>(
                                            `<span class="mode__name">
                                                ${modeChoices[item]}
                                            </span>`
                                        )).join(' ')}
                                    </div>`:''
                        }
                              
                        ${products[key].pPvn ?
                                `<div class="provider">
                                  Provider 
                                  <span class="provider__name">
                                    ${products[key].pPvn}
                                  </span>
                                </div>`:''
                        }
                    </div>

                    <div class="mr-auto courses">
                        <strong class="courses__price">Rs. ${ Math.round((products[key].pPin)*100)/100 }/-</strong>
                    </div>
                    
                    ${products[key].pTg ==1 ?
                        `<div class="course-tag">
                            <span class="course-tag__best">Bestseller</span>
                        </div>`:
                    products[key].pTg ==  2?
                        `<div class="course-tag">
                            <span class="course-tag__new">Newly Added</span>
                        </div> `:''
                    }
                </li>
            `)
        }
        loaderDiv.addClass('d-none');
        !data.next ? $(el).parent().hide():$(el).show();

    })
}

// submit need help form
const needHelpFormSubmit = (formData,lsource) => {
    $.post(`/lead/lead-management/`,formData,(data)=>{
        lsource[0] ? gaEventFunc(lsource[0].value,'success'):''
        Toast.fire({
            type: 'success',
            title: 'A callback will be arranged from executive'
        })
        $("#callUsForm").find("input[type=text]").val("");
	    
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
    $('#faq-accordion').children('.card').each(function(){
        $(this).removeClass('d-none')
    })
    $('#more-faq').addClass('d-none')
}

//Funtion used to set activate of sticky nav while scrolling
const stickyNavbarActiveScroll = (startStickyActiveScroll) => {
    var topMenu = $("#navbarNav"),
    topMenuHeight = topMenu.outerHeight()+15,
    // All list items
    menuItems = topMenu.find("a"),
    // Anchors corresponding to menu items
    scrollItems = menuItems.map(function(){
      var item = $($(this).attr("href"));
      if (item.length) { return item; }
    });

    var showStickyNavbarHandler = () =>{
        $('.sticky-nav')[$(window).scrollTop() >= aboutSectionPosTop ? 'removeClass' : 'addClass']('sticky-none');
    }
    
    var scrollHandler = () => {
        // Get container scroll position
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
        }
    }
    // Bind to scroll
    startStickyActiveScroll ? $(window).on('scroll',scrollHandler) : $(window).off('scroll')
    $(window).on('scroll',showStickyNavbarHandler)
   
}

// funtion to set rukes and validate need help form
const needHelpFormValidation = () => {

    var callUsForm = $("#callUsForm");
    $("#callUsForm").validate({
        errorClass:'error-msg',
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

// function to add a new validation rules of letters only in jquery validate
const lettersOnlyValidator = () => {
    $.validator.addMethod("lettersonly", function(value, element) {
        return this.optional(element) || /^[a-z," "]+$/i.test(value);
    }); 
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