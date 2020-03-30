


import { siteDomain } from "../Utils/domains";


const defaultHeaders = {
    "Content-Type": "application/json",
};

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
