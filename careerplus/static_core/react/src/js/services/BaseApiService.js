const defaultHeaders = {
    "Content-Type": "application/json"
}

// todo make seperate function for fetch request

const get = (url, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'GET',
    })
        .then(response => response.json())
        .then(handleResponse)
}


const post = (url, data, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(handleResponse)
}

const put = (url, data, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(handleResponse)
}


function handleResponse(response) {
    // handle all the status and conditions here

    return response;
}


export default {
    get,
    post,
    put
}