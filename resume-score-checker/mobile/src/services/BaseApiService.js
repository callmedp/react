import { siteDomain } from "../Utils/domains";

const defaultHeaders = {
    "Content-Type": "application/json",
}

// todo make seperate function for fetch request

const get = (url, headers = {
    ...defaultHeaders,
}, isFetchingHTML = false) => {
    return fetch(url, {
        headers,
        method: 'GET'
    })
        .then(response => response.json())
        .catch(e => { throw e })
        // .then(async (response) => {
        //     return await handleResponse(response, isFetchingHTML)
        // })
};

const post = (url, data, headers = {
    ...defaultHeaders,
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : data
    })
        .then(response => response)
        .catch(e => { throw e})
};

// async function handleResponse(response, isFetchingHTML) {
//     // handle all the status and conditions here
//     if (response['ok'] === false) {
//         let message = '';
//         let data = await response.json();
//         for (const key in data) {
//             message += `${data[key]} `;
//         }
//         return {
//             error: true,
//             errorMessage: message,
//             status: response['status'],
//         }
//     } else if (response['status'] === 204) {
//         return {data: {}};
//     } else {
//         let result = isFetchingHTML ? await response.text() : await response.json();
//         return { data: result };
//     }
// }


export default {
    get,
    post
}