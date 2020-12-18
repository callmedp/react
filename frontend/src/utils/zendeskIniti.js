// Initialize Zendesk Chat
export const initZendesk = async () =>
  new Promise(resolve => {
        window.$zopim || (function (d, s) {
          var z = window.$zopim = function (c) { z._.push(c) }, $ = z.s =
              d.createElement(s), e = d.getElementsByTagName(s)[0]; z.set = function (o) {
                  z.set.
                      _.push(o)
              }; z._ = []; z.set._ = []; $.async = !0; $.setAttribute("charset", "utf-8");
          $.src = "https://v2.zopim.com/?5xDfzOy1OsJEYM1rLRdXyvsf3GOj6Qmb"; z.t = +new Date; $.
              type = "text/javascript"; e.parentNode.insertBefore($, e)
        })(document, "script");

        window.$zopim(function() {
            window.$zopim.livechat.hideAll();
            resolve(true);
        });
  });

// Setting Value in the Zendesk Chat if the user is Logged in
export const initLoggedInZendesk = (candidateDetails) => {
    if (candidateDetails) {
        const full_name = candidateDetails?.full_name;
        const  email = candidateDetails?.email;
        const mobile_no = candidateDetails?.mobile_no;
            
        window && window.$zopim &&  window.$zopim(function () {
            window.$zopim.livechat.set({
                language: 'en',
                name: full_name ? full_name.charAt(0).toUpperCase() + full_name.slice(1): '',
                email: email ? email : '',
                phone: mobile_no ? mobile_no : ''
            });                
        });
    }
}

//Show Zendesk Chat Window on Click
export const zendeskChatShow = () => {
    window.$zopim(function () {
        window.$zopim.livechat.window.show();
        window.$zopim.livechat.window.onHide(function () {
            window.$zopim.livechat.hideAll()
        })
    });
}

//Show Zendesk Chat Window after "time interval" 
export const zendeskTimeControlledWindow = (timeinterval = 700) => {
    setTimeout(() => {
        window && window.$zopim &&  window.$zopim.livechat.window.show();
    }, timeinterval)
}