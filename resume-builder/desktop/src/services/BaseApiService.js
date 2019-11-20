import { siteDomain } from "../Utils/domains";

const defaultHeaders = {
    "Content-Type": "application/json",
    'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : ''
};

// todo make seperate function for fetch request

const get = (url, headers = {
    ...defaultHeaders,
    ...{ 'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : '' }
}, isFetchingHTML = false) => {
    return fetch(url, {
        headers,
        method: 'GET'
    })
        // .then(response => response.json())
        .then(async (response) => {
            return await handleResponse(response, isFetchingHTML)
        })
        .catch(err => console.log(err))
};

const handleParams = (data) => Object.keys(data).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
}).join('&');

const post = (url, data, headers = {
    ...defaultHeaders,
    ...{ 'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : '' }
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then(handleResponse)
        .catch(err => console.log(err))
};

const patch = (url, data, headers = {
    ...defaultHeaders,
    ...{ 'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : '' }
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'PATCH',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then(handleResponse)
        .catch(err => console.log(err));
};

const deleteMethod = (url, headers = {
    ...defaultHeaders,
    ...{ 'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : '' }
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'DELETE',
    })
        .then(handleResponse)
        .catch(err => console.log(err));
};

const put = (url, data, headers = {
    ...defaultHeaders,
    ...{ 'Authorization': (typeof localStorage !== 'undefined') ? localStorage.getItem('token') || '' : '' }
}, isStringify = true) => {
    return fetch(url, {
        headers,
        method: 'PUT',
        body: isStringify ? JSON.stringify(data) : data
    })
        .then(handleResponse)
        .catch(err => console.log(err));
};


async function handleResponse(response, isFetchingHTML) {

    // handle all the status and conditions here
    if (response['ok'] === false) {
        let message = '';
        let data;
        try {
            data = await response.json();
            for (const key in data) {
                message += `${data[key]} `;
            }
            if (response['status'] === 401) {
                window.location.href = `http://localhost:3000/resume-builder/?login=false`;
            }
            return {
                error: true,
                errorMessage: message,
                status: response['status'],
            }

        } catch (e) {
            console.log('--error--', e);
            return {
                error: true,
                errorMessage: 'Something went wrong',
                status: response['status'],
            }
        }

    } else if (response['status'] === 204) {
        return { data: {} };
    } else {
        let result = isFetchingHTML ? await response.text() : await response.json();
        return { data: result };
    }
}


export default {
    get,
    post,
    put,
    deleteMethod,
    patch
}