/*
Common function used in this file:
1. Typeahaed :
    a) typeAheadSource => create a bloodhound objeect with dataset for typeahead
    b) attachTypeaheadElementDom => Attach typeahead feature to an element in dom.
2. Toast => Sweetalert2 toast
3. smoothScrolling => Smooth scrolling for an element to a particular div
4. GA functions
    a) get analytics script
    b) ga event raise

*/

$(document).ready(()=>{
})

/*
Typeahead functions
*/
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

const smoothScrolling = (id,extraOffset) => {
    extraOffset = extraOffset ? extraOffset : 0
    $('html, body').animate({
        scrollTop: $(`#${id}`).offset().top + extraOffset
    }, 'slow');
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


