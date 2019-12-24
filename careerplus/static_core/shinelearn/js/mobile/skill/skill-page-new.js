let coursePageNo = 2,assessmentPageNo=2  //the page no starts form 2 cause 1st page is already loaded
let pageSize = 5
let categoryId = null


$(document).ready(()=>{
    //categoryid and heading form couse list attributes
    categoryId = $('#tab-bar').attr('categoryId');
    stickyNavbarActiveScroll()
})

const changeTab = (setTabId,removeTabId) => {
    console.log('Here')
    $(`#${setTabId}`).addClass('current')
    $(`#${removeTabId}`).removeClass('current')
    $(`#${setTabId}-text`).addClass('current')
    $(`#${removeTabId}-text`).removeClass('current')
}

//load courses or assessment 
//arg1 : el => used to remove the button when more products cannot be loaded
//arg2 : type => deciding whether course or product to be loaded
//This function sends a get request to get products and append them to dom
const loadProduct = (el,type) => {
    console.log(categoryId)
    const pTFInclude = type==='course'?false:true
    const pageNo = type==='course'?coursePageNo:assessmentPageNo
    const productTypeId = type==='course'?'#tab-1':'#tab-2'

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
        
        if(!data.next){
            $(el).parent().hide()
        }
        
        for (key in products){
            $(productTypeId).find('ul').append(`
                <li class="d-flex row">
                    <span class="skill-tabs--image">
                        <img aria-label="${products[key].pNm}" src="${products[key].pImg}" alt="${products[key].pNm}">
                    </span><!-- // Image -->

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

    })
}


//Open More FAQ
const openMoreFAQ = () =>{    
    $('.css-accordion').children('.css-accordion--tab').each(function(){
        $(this).removeClass('hide')
    })
    $('#more-faq').addClass('hide')
}


const stickyNavbarActiveScroll = () => {
    debugger
    var topMenu = $("#sticky-header"),
    topMenuHeight = topMenu.outerHeight()+15,
    // All list items
    menuItems = topMenu.find("a"),
    // Anchors corresponding to menu items
    scrollItems = menuItems.map(function(){
      var item = $($(this).attr("href"));
      if (item.length) { return item; }
    });

    // Bind to scroll
    // $(window).scroll(function(){
    // // Get container scroll position
    // var fromTop = $(this).scrollTop()+topMenuHeight;

    // // Get id of current scroll item
    // var cur = scrollItems.map(function(){
    //     if ($(this).offset().top < fromTop)
    //     return this;
    // });
    // // Get the id of the current element
    // cur = cur[cur.length-1];
    // var id = cur && cur.length ? cur[0].id : "";
    // // Set/remove active class
    // menuItems
    //     .parent().removeClass("active")
    //     .end().filter("[href='#"+id+"']").parent().addClass("active");
    // });​
}