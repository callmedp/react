const defaultHeaders = {
    "Content-Type": "application/json",
    'Authorization': "5ab9b90da69bd53cec4cf20559f9052b24325c7e"
};

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

const post = (url, data, headers = defaultHeaders, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then(handleResponse)
};

const deleteMethod = (url, headers = defaultHeaders, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'DELETE',
    })
        .then(handleResponse)
};

const put = (url, data, headers = defaultHeaders, isStringify = true) => {
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