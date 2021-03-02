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
    return fetch(`${siteDomain}/intent/api/v1/keyword-suggestion/?q=${search}&jt_only=true`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            // return [{"pid":"1307109","pdesc":"python","alias":"python","type":"skill"},{"pid":"5188","pdesc":"pyramid it consulting","alias":"pyramid it consulting"},{"pid":"55729","pdesc":"pyrotech electronics","alias":"pyrotech electronics pvt. ltd, udaipur"},{"pid":"73971","pdesc":"pyro networks","alias":"pyro networks, hyderabad"},{"pid":"88234","pdesc":"pyramid saimira theatre","alias":"pyramid saimira theatre ltd"},{"pid":"106430","pdesc":"pyramid consulting inc","alias":"pyramid consulting inc."},{"pid":"111339","pdesc":"pyxis systems","alias":"pyxis systems pvt ltd"},{"pid":"112998","pdesc":"pyramid","alias":"pyramid"},{"pid":"120897","pdesc":"pyramid consulting engineers","alias":"pyramid consulting engineers"},{"pid":"134149","pdesc":"pyramid technologies","alias":"pyramid technologies"}]
            return [];
        }
    );

}

const relatedSearch = (query) =>{
    // return fetch(`${siteDomain}/intent/api/v1/keyword-suggestion/?q=${query}&skill_only=true`,
    return fetch(`https://sumosc.shine.com/api/v3/search/skill-to-related-skills/?q="${query}"`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            // return ["Django","C","C++","Machine Learning","Java","Bash","Perl","Software Engineering","Linux","Python Professional","Python Expert","Developer","Technical Lead","Numpy","Scipy","Sqlalchemy","Pyqt","Celery","Matplotlib","Scikit-Learn","Twisted"]
            return [];
        }
    );

}

const userSkillSearch = (query) =>{
    return fetch(`${siteDomain}/intent/api/v1/keyword-suggestion/?q=${query}&skill_only=true`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            return [];
        }
    );

}

export {
    searchCharacters,
    submitData,
    userSearch,
    relatedSearch,
    userSkillSearch
}