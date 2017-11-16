$(document).on("click","a[href^='tel']",function(){
    MyGA.SendEvent('CallbackRequested', 'Call Interactions', 'General Enquiry', 'success');
});