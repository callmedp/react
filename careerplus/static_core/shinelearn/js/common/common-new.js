$(document).ready(()=>{
    //typeahead for search box new skill page
    //Note: Add class search-box in search box 
    attachTypeaheadElementDom('.search-box')
    navigationDropdownHelper()
    
})

const navigationDropdownHelper = () =>{
    //hover method for better navigation
    $('.category-tab .nav-tabs > li ').hover(function() {
        if ($(this).hasClass('hoverblock')){
            return;
        }
        else{
            if(previous_tab){
                $(`${previous_tab.attr('data-target')}`).removeClass('active')
                $(`${previous_tab.attr('data-target')}`).removeClass('show')
            }
            $(this).find('a').tab('show');
            previous_tab = $(this).find('a')
        }
    },function(){}).click(function(){
        window.location.replace($(this).find('a').attr('href'))
    });
}

const typeAheadSource = (dataSet) =>{
    return new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local:Object.keys(dataSet)
    });
} 

const attachTypeaheadElementDom = (el) =>{
    //Note: attach type ahead directly to input
    $(el).typeahead(
        {
            highlight: false
        },
        {
            name: 'category_skill',
            source: typeAheadSource(categoryUrlSet),
            limit: 3,
            templates: {
                header: '<h3>Skills</h3>'
            }
        },
        {
            name: 'products',
            source: typeAheadSource(productUrlSet),
            limit: 3,
            templates: {
                header: '<h3>Products</h3>'
            }
        }
    ).bind('typeahead:select', function(ev, suggestion) {
        if (categoryUrlSet[suggestion]) 
            window.location.href = `${categoryUrlSet[suggestion]}`;
        else 
            window.location.href = `${productUrlSet[suggestion]}`;
    });
}

// Toast function
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});

const smoothScrolling = (id) => {
    $('html, body').animate({
        scrollTop: $(`#${id}`).offset().top
    }, 700);
}


  