
let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5
let categoryId = null
let timeoutID = null


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

    stickyNavbarActiveScroll(true) //true argument is to start active scroll
    objectiveDivCollasedHeightSet()
    callUsFormDataValidation()
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

        if(!data.next){
            $(el).hide()
            $(el).parent().hide()
        }
        
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

    })
}

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



//ga functions
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create', 'UA-3537905-41', 'auto', {'name': 'a'});
    ga('a.send', 'pageview');
    ga('create', 'UA-3537905-41', 'auto');
    ga('send', 'pageview');

const gaEvent = (event_cat,event_lab,event_action) =>{
    ga('send', 'event', event_cat, event_action, event_lab);
}

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
        $('.sticky-nav')[$(window).scrollTop() >= 420 ? 'removeClass' : 'addClass']('sticky-none');
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


//fucntion to dynamically set height for objective to show only 3 items
const objectiveDivCollasedHeightSet = () => {
    let objectiveLiELements = $('.objective__list').find('li').slice(0,3);
    let totalWidth = 0
    for(el of objectiveLiELements){
        totalWidth+=$(el).outerHeight(true)
    }
    $('.objective__list').css({'height':totalWidth})
    $('.objective__list').on('hidden.bs.collapse', function () {
        $(this).css({'height':totalWidth})
    })
}



const callUsFormDataValidation = () => {

    var callUsForm = $("#callUsForm");
    callUsForm.validate({
        errorClass:'error-msg',
        rules: {
            name: {
                required: true,
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

const indiaMobileValidator = () => {
    $.validator.addMethod("indiaMobile", function(value) {
        var country_code = $('#country-code').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });
}