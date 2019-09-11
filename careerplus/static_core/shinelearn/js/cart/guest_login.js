$(document).ready(function () {
    var login_button = document.getElementById("login_guests")

    if (login_button != null) {
        login_button.addEventListener("click", guest_login);
    }


    async function guest_login() {
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r;
            i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date();
            a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
            a.async = 1;
            a.src = g;
            m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
        ga('create', 'UA-3537905-41', 'auto', {'name': 'a'});
        ga('a.send', 'pageview');
        ga('create', 'UA-3537905-41', 'auto');
        ga('send', 'pageview');

        function hitGA() {
            ga('send', 'event', 'Cart Order Login', 'Buy Flow', 'Continue as Guest');
        }


        var form = document.getElementById('guest_form');
        const guest_info = $(form).serializeArray().reduce((obj, elem) => {
            obj[elem.name] = elem.value
            return obj;
        }, {})
        hitGA();
        let email = guest_info['email'] || '';
        if ($('#guest_form').valid()) {
            // let isEmailRegistered = await checkEmailExists(email)
            // if (isEmailRegistered) {
            //     $('#email-error').html('This email already exists. Please register with some other email.');
            //     $('#email-error').closest('.form-group').addClass('error1');
            //     return;
            // }
            let input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "login_with");
            input.setAttribute("value", "login_guest")
            form.appendChild(input);
            form.submit();
        }


    }

    const checkEmailExists = async (email = '') => {
        //  create an api to check whether a user has registered email or not
        const result = await fetch(`${site_domain}/api/v1/cart/email-status/${email}/`)
        const {exists} = await result.json();
        return exists

    };
    /*
    * Fetch Country List
    * */
    const fetchCountryList = () => {
        $('#country_code').select2({
            placeholder: 'Search Country',
            ajax: {
                delay: 300,
                url: `${site_domain}/api/v1/geolocation/country/`,
                data: function (params) {

                    let query = {
                        page: params.page || 1,
                        page_size: 10,
                        search: (params.term || '').trim()
                    };
                    return query;
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.results.map(country => ({
                            id: country['phone'], text: `${country['name']}(+${country['phone']})`
                        })),
                        pagination: {
                            more: (params.page * 10) < data.count
                        }
                    };
                }
            },
            templateSelection: function (element) {
                return `+${element.id}`;
            },
            dropdownAutoWidth: true

        })
    };


    fetchCountryList();

})
