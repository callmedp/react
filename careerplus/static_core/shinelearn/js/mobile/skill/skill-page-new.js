let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5
let categoryId = null


$(document).ready(()=>{
    //categoryid and heading form couse list attributes
    categoryId = $('#tab-1').attr('categoryId');

})

const changeTab = (setTabId,removeTabId) => {
    console.log('Here')
    $(`#${setTabId}`).addClass('current')
    $(`#${removeTabId}`).removeClass('current')
    $(`#${setTabId}-text`).addClass('current')
    $(`#${removeTabId}-text`).removeClass('current')
}

const loadProduct = (type) => {
    const pTFInclude = type==='course'?false:true
    const pageNo = type==='course'?coursePageNo:assessmentPageNo
    const productTypeId = type==='course'?'#tab-1':'#tab-2'

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
            $(productTypeId).find('ul').append(`
                <li class="d-flex row">
                    <span class="skill-tabs--image">
                        <img aria-label="${products[key].pNm}" src="${products[key].pImg}" alt="${products[key].pNm}">
                    </span><!-- // Image -->

                    <div class="skill-tabs__content">
                        <div class="skill-tabs__content--tag skill-tabs__content--bestseller">Bestseller</div>
                        <a class="d-block pt-5" href="${products[key].pURL}"><strong>${products[key].pNm}</strong></a>
                        <div class="ratingView mt-10">
                            <span class="rating" data-rating="${ Math.round((products[key].pARx)*100)/100 }"></span> 
                            ${ Math.round((products[key].pARx)*100)/100 }/5
                        </div>
                        <div class="skill-tabs__content--mode">
                            Mode
                            <span>Instructor</span>
                            <span>Online</span>
                        </div><!-- // mode -->
                        <p class="skill-tabs__content--provider fs-11"><small class="mr-5">Provider</small>${products[key].pPvn}</p>
                        <p class="skill-tabs__content--price"><strong>Rs. ${ Math.round((products[key].pPin)*100)/100 }/- </strong></p>
                    </div>
                </li>
            `)
        }

    })
}


//Open More FAQ
const openMoreFAQ = () =>{    
    $('.css-accordion').children('.css-accordion--tab').each(function(){
        $(this).removeClass('hide')
    })
    $('#more-faq').addClass('hide')
}