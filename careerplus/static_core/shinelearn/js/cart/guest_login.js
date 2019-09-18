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
        ga('create', 'UA-3537905-41', 'auto', { 'name': 'a' });
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
        const { exists } = await result.json();
        return exists

    };

    $('#country_code').on('select2:select', function (e) {
        let data = e.params.data
        if (data && data.id && data.id === "91") {
            $("#guest-mobile").rules("add", {
                required: true,
                digits: true,
                indiaMobile: true,
                minlength: 10,
                maxlength: 10,
                messages: {
                    required: 'Contact is required.',
                    digits: 'only digit accepted.',
                    indiaMobile: 'length must be 10 digits.',
                    minlength: 'length must be 10 digits.',
                    maxlength: 'length must be 10 digits.',
                }
            });
        }
        else {
            $("#guest-mobile").rules("add", {
                required: true,
                digits: true,
                indiaMobile: true,
                minlength: 6,
                maxlength: 13,
                messages: {
                    required: 'Contact is required.',
                    digits: 'only digit accepted.',
                    indiaMobile: 'length must be 10 digits.',
                    minlength: 'length must be greater than 3 digits.',
                    maxlength: 'length must be less than 15 digits.',
                }
            });
        }
    });
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
                    params.term = (params.term || '').trim()
                    params.term = params.term && params.term[0] === '+' ? params.term.substring(1) : params.term
                    let query = {
                        page: params.page || 1,
                        page_size: 10,
                        search: params.term
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

    /*
     - auto fill the fields of the guest page, if the details of the user is available in the current cart. 
    */



    // auto fill the form if we have person details


    const autoFillGuestDetails = () => {

        let info = cartData.split(',');

        const formObj = {
            'name': info[0],
            'email': info[1],
            'country_code': info[2],
            'mobile': info[3]
        }
        document.forms['guest_form'].elements['name'].value = formObj['name'].trim() || ''
        if (formObj['name'].trim()) $("#guest_form input#guest-name").addClass('has-content');
        document.forms['guest_form'].elements['email'].value = formObj['email'].trim() || ''
        if (formObj['email'].trim()) $("#guest_form input#guest-email").addClass('has-content');
        const ccVal = formObj['country_code'] || '91';
        if ($('#country_code').find("option[value='" + ccVal + "']").length) {
            $('#country_code').val(ccVal).trigger('change');
        } else {
            // Create a DOM Option and pre-select by default
            var newOption = new Option(`+${ccVal}`, ccVal, true, true);
            // Append it to the select
            $('#country_code').append(newOption).trigger('change');
        }
        document.forms['guest_form'].elements['mobile'].value = formObj['mobile'].trim() || ''
        if (formObj['mobile'].trim()) $("#guest_form input#guest-mobile").addClass('has-content');






    }

    autoFillGuestDetails();




})
