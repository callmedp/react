const defaultHeaders = {
    "Content-Type": "application/json"
}

// todo make seperate function for fetch request

const get = (url, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'GET',
    })
    // .then(response => response.json())
        .then(handleResponse)
}

const handleParams = (data) => Object.keys(data).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
}).join('&');

const post = (url, data, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body:  handleParams(data)
    })
        .then(handleResponse)
}

const put = (url, data, headers = defaultHeaders) => {
    return fetch(url, {
        headers,
        method: 'PUT',
        body: data
    })
        .then(handleResponse)
}


async function handleResponse(response) {
    // handle all the status and conditions here
    if (response['ok'] === false) {
        let message = '';
        let data = await response.json();
        for (const key in data) {
            message += `${data[key]} `;
        }
        return {
            error: true,
            errorMessage: message,
            status: response['status'],
        }
    } else {
        let result = await response.json();
        return {data: result};
    }
}


export default {
    get,
    post,
    put
}