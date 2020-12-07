import { FETCH_NAVIGATION_OFFERS_AND_SPECIAL_TAGS  } from './actionTypes';

const fetchNavOffersAndTags = (payload) => {
    return {
        type : FETCH_NAVIGATION_OFFERS_AND_SPECIAL_TAGS,
        payload
    }
}

export {
    fetchNavOffersAndTags,
}