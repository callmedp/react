
const defaultHeaders = {
    "Content-Type": "application/json",
};


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
        .catch(err =>{ throw err } )
};

const post = (url, data, headers = {
    ...defaultHeaders,
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then( response => response.json() )
        .catch(err =>{ throw err } )
        
};


export default {
    post,
    get
}