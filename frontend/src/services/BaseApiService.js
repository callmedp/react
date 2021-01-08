// import { siteDomain } from "../Utils/domains";
import { getLearningToken, getAccessKey } from "utils/storage";

const getHeaders = () => {
        return {
            "Content-Type": "application/json",
            'Authorization': getLearningToken(),
            'Access-key': getAccessKey()
        }

}

const defaultHeaders = getHeaders()

// todo make seperate function for fetch request

const get = (url, headers = getHeaders()
, isFetchingHTML = false) => {
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


const post = (url, data, headers = getHeaders(), upload = false, stringify = true) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: upload ? data : stringify ? JSON.stringify(data) : handleParams(data)
    })
    .then(handleResponse)
    .catch(err => console.log(err))
};

const patch = (url, data, headers = {
    ...defaultHeaders,
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
    "Content-Type": "application/json",
    'Authorization': getLearningToken(),
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
            return {
                error: true,
                ...data,
                status : response.status,
            }
            
        } catch (e) {
            
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