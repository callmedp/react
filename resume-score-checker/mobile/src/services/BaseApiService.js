
const defaultHeaders = {
    "Content-Type": "application/json",
}

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
        body: isStringify ? JSON.stringify(data) : isUpload ? data : data
    })
        .then(handleResponse)
        .catch(e => { throw e})
};

async function handleResponse(response) {

    if (response['status'] === 0) {
            return {
                error: true,
                errorMessage: "Unable to parse your resume. Please Upload new Resume",
                status: response['status']
            }
    }
    else{
        throw response;
    }
}

export default {
    get,
    post
}