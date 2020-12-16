import { siteDomain } from '../domains'

// API search function
const searchCharacters = search =>{
    return fetch(`${siteDomain}/api/v1/search-query/?q=${search}`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            return [];
        }
    );
}

const submitData = (values, event) => {
    const searchedQuery = values?.query
    if(searchedQuery){
        window.location.push(`${siteDomain}/search/results/?q=${searchedQuery}`);
    }
}

export {
    searchCharacters,
    submitData
}