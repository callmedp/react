
const defaultHeaders = {
    "Content-Type": "application/json",
}

const handleParams = (data) => Object.keys(data).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
}).join('&');

const get = (url, headers = {
    ...defaultHeaders,
}, isFetchingHTML = false) => {
    return fetch(url, {
        headers,
        method: 'GET'
    })
        .then(response => response.json())
        .catch(e => { throw e })
};

const post = (url, data, headers = {
    ...defaultHeaders,
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data :handleParams(data)
    })
        .then(handleResponse)
        .catch(e => { throw e })
};

async function handleResponse(response) {

    if (response['error_message']) {
            return {
                error: true,
                errorMessage: response['error_message']
            }
    }
    else{
        return response;
    }
}

export default {
    get,
    post
}