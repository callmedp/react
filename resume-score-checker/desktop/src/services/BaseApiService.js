


const defaultHeaders = {
    "Content-Type": "application/json",
};


const handleParams = (data) => Object.keys(data).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
}).join('&');



const post = (url, data, headers = {
    ...defaultHeaders,
}, isStringify = true, isUpload = false) => {
    return fetch(url, {
        headers,
        method: 'POST',
        body: isStringify ? JSON.stringify(data) : isUpload ? data : handleParams(data)
    })
        .then(data => data)
        .catch(err => console.log(err))
        
};



// async function handleResponse(response, isFetchingHTML) {

//     // handle all the status and conditions here
//     if (response['ok'] === false) {
//         let message = '';
//         let data;
//         try {
//             data = await response.json();
//             for (const key in data) {
//                 message += `${data[key]} `;
//             }
//             if (response['status'] === 401) {
//                 window.location.href = `${siteDomain}/resume-builder/?login=false`;
//             }
//             return {
//                 error: true,
//                 errorMessage: message,
//                 status: response['status'],
//             }

//         } catch (e) {
//             console.log('--error--', e);
//             return {
//                 error: true,
//                 errorMessage: 'Something went wrong',
//                 status: response['status'],
//             }
//         }

//     } else if (response['status'] === 204) {
//         return { data: {} };
//     } else {
//         let result = isFetchingHTML ? await response.text() : await response.json();
//         return { data: result };
//     }
// }



export default {
    post,
}