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
5. showHideElement => //show or remove a element with fadeIn and fadeOut animation from DOM
6. needHelpFormFocus => Focus class added when clicking an element in needHelpForm
*/

$(document).ready(()=>{
    needHelpFormFocus();
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
            name: 'course',
            source: typeAheadSource(courseUrlSet),
            limit: 3,
            templates: {
                header: '<h3>Courses</h3>'
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
        else if (productUrlSet[suggestion])
            window.location.href = `${productUrlSet[suggestion]}`;
        else
            window.location.href = `${courseUrlSet[suggestion]}`;
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

//show or remove a element with fadeIn and fadeOut animation from DOM
const showHideElement = (showElement,id) => {
	showElement ? $(`#${id}`).delay(100).fadeIn() : $(`#${id}`).delay(100).fadeOut()
}


// move elements up on focus in needHelpForm
const needHelpFormFocus = () =>{
    $("#enquire").find('input').focus(function(){
        $("#enquire").addClass("enquire-focus")     
    }).blur(function(){
        $("#enquire").removeClass("enquire-focus")
    })
}

const makeTrackingRequest = (loggingData) => {
    $.ajax({
        method: "POST",
        url: `${shineApiUrl}/learning-touchpoints-tracking/`,
        data: JSON.stringify(loggingData),
        contentType: "application/json",
    })
}

const skillpageTracking = (action) => {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action, 'position': position, domain: 2, sub_product: trackingProductId, trigger_point: trigger_point, u_id: candidate_id, utm_campaign: utm_campaign, popup_based_product: popup_based_product };
    if (trackingId) {
        makeTrackingRequest(loggingData);
    }
}
