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

const submitData = (values) => {
    const searchedQuery = values?.query
    if(searchedQuery){
        window.location.href = `${siteDomain}/search/results/?q=${searchedQuery}`;
    }
}

const userSearch = (search ) =>{
    return fetch(`https://www.shine.com/api/v3/search/lookup/keyword-suggestions/query/?q=${search}`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            return [{"pid":"1307109","pdesc":"python","alias":"python","type":"skill"},{"pid":"5188","pdesc":"pyramid it consulting","alias":"pyramid it consulting"},{"pid":"55729","pdesc":"pyrotech electronics","alias":"pyrotech electronics pvt. ltd, udaipur"},{"pid":"73971","pdesc":"pyro networks","alias":"pyro networks, hyderabad"},{"pid":"88234","pdesc":"pyramid saimira theatre","alias":"pyramid saimira theatre ltd"},{"pid":"106430","pdesc":"pyramid consulting inc","alias":"pyramid consulting inc."},{"pid":"111339","pdesc":"pyxis systems","alias":"pyxis systems pvt ltd"},{"pid":"112998","pdesc":"pyramid","alias":"pyramid"},{"pid":"120897","pdesc":"pyramid consulting engineers","alias":"pyramid consulting engineers"},{"pid":"134149","pdesc":"pyramid technologies","alias":"pyramid technologies"}]
            // return [];
        }
    );

}

export {
    searchCharacters,
    submitData,
    userSearch
}