let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5
let categoryId = null
let needHelpFormValues = { //default values required for lead management
    'country':'91', //by default country code=91 for india
    'path':window.location.href,  //absolute path of the current url
    'lsource':1, //default value for skill page
    'number':'',
    'email':'',
    'name':'',
} 
let needHelpFormError = false


$(document).ready(()=>{
    //for form values recieving categoryid and heading form couse list attributes
    categoryId = $('#course-list').attr('categoryId');
    let categoryHeading = $('#course-list').attr('categoryHeading');
    needHelpFormValues['prd'] = categoryHeading
    needHelpFormValues['product'] = categoryId

    //hover method for better navigation
    $('.category-tab .nav-tabs > li ').hover(function() {
        if ($(this).hasClass('hoverblock'))
          return;
        else
          $(this).find('a').tab('show');
    });

    $(window).on('scroll', function (e) {
        $('.sticky-nav')[$(window).scrollTop() >= 420 ? 'removeClass' : 'addClass']('sticky-none');
    })

    $('.sticky-nav .nav-link').click(function(){
        $('.sticky-nav .nav-link').removeClass('active');
        $(this).addClass('active');
    })



})

const loadProduct = (type) => {
    const pTFInclude = type==='course'?false:true
    const pageNo = type==='course'?coursePageNo:assessmentPageNo
    const productTypeId = type==='course'?'#course-list':'#assessment-list'

    $.get(`api/v1/load-more/`,
    {
        "page": pageNo, "page_size": pageSize, "pCtg" : categoryId, 
        "pTF" : 16 ,"pTF_include" : pTFInclude,  
        "fl" : "name,pCert,pURL,pImg,pNm,pNJ,pHd,pStar,pARx,pPin,pPfin,pPvn,discount,pAsft"
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

                        <div class="mode mr-30">
                            Mode 
                            <span class="mode__name">
                                Instructor
                            </span>
                        </div>
                        <div class="provider">
                            Provider 
                            <span class="provider__name">
                                ${products[key].pPvn}
                            </span>
                        </div>
                    </div>

                    <div class="mr-auto courses">
                        <strong class="courses__price">Rs. ${ Math.round((products[key].pPin)*100)/100 }/-</strong>
                    </div>

                    <div class="course-tag">
                        <span class="course-tag__best">Bestseller</span>
                    </div>
                </li>
            `)
        }

    })
}

const needHelpFormSubmit = () => {
    checkError()
    if (needHelpFormError)
        return
    needHelpFormValues.country = $('#country-code').val()
    
    $.post(`/lead/lead-management/`,needHelpFormValues,(data)=>{
        gaEventFunc(needHelpFormValues.lsource,'success');
        Toast.fire({
            type: 'success',
            title: 'A callback will be arranged from executive'
        })
	    
    }).fail(()=>{
        gaEventFunc(needHelpFormValues.lsource,'failure');
        Toast.fire({
            type: 'error',
            title: 'Something went wrong'
        })
    })

}

const checkError = () => {
    for(key in needHelpFormValues){
        value = needHelpFormValues[key]
        switch(key){

            case 'number':{
                errorName = !value ? 'Required':value.length<4?'Min length is 4':value.length>16?'Max length is 15':''
                errorName ? showError(key,errorName):()=>{} 
                break
            }
            case 'email':{
                errorName = !value ? 'Required':!isEmailValidation(value)?'Invalid Email':''
                errorName ? showError(key,errorName):()=>{} 
                break
            }
            case 'name':{
                errorName = !value ? 'Required':value.length<2?'Min length is 2':value.length>51?'Max length is 50':''
                errorName ? showError(key,errorName):()=>{} 
                break
            }
            default:
                break
        }
    }
}

const showError = (id,errorName) =>{
    needHelpFormError = true
    let parent = $(`#${id}`).parent()
    parent.children('.error-msg').text(errorName)
    parent.children('.error-msg').removeClass('d-none')
    parent.addClass('error') 
}

const removeError = (id) => {
    needHelpFormError = false
    let parent = $(`#${id}`).parent()
    parent.children('.error-msg').addClass('d-none')
    parent.removeClass('error') 
}

const updateValueFormInput = (el,id) => {
    needHelpFormValues[`${id}`] =  $(el).val()
    removeError(id)
}

//Validation functions
const lengthValidation = (val,min,max)=>{
    if(val.length>=min && val.length<=max)
        return true
    return false
}

const isEmailValidation = (email) => {
    let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
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

// Toast finction
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});


//Open More FAQ
const openMoreFAQ = () =>{
    console.log('HERE')
    
    $('#faq-accordion').children('.card').each(function(){
        $(this).removeClass('d-none')
    })
    $('#more-faq').addClass('d-none')
}