const defaultHeaders = {
    "Content-Type": "application/json",
};

const rudDefaultHeaders = {
    "Content-Type": "application/json",
    'authorization': "0c05804dcb70a3ce4e08f95a545bce120ee370ab"

}

// todo make seperate function for fetch request

const get = (url, headers = defaultHeaders, isFetchingHTML = false) => {
    return fetch(url, {
        headers,
        method: 'GET'
    })
    // .then(response => response.json())
        .then(async (response) => {
            return await handleResponse(response, isFetchingHTML)
        })
};

const handleParams = (data) => Object.keys(data).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
}).join('&');

const post = (url, data, headers = rudDefaultHeaders, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then(handleResponse)
};

const deleteMethod = (url, headers = rudDefaultHeaders, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'DELETE',
    })
        .then(handleResponse)
};

const put = (url, data, headers = rudDefaultHeaders, isStringify = true) => {
    return fetch(url, {
        headers,
        method: 'PUT',
        body: isStringify ? JSON.stringify(data) : data
    })
        .then(handleResponse)
};


async function handleResponse(response, isFetchingHTML) {

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
    } else if (response['status'] === 204) {
        return {data: {}};
    } else {
        let result = isFetchingHTML ? await response.text() : await response.json();
        return {data: result};
    }
}


export default {
    get,
    post,
    put,
    deleteMethod
}