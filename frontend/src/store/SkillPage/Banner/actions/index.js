import { FETCH_SKILL_PAGE_BANNER  } from './actionTypes';

const fetchSkillPageBanner = (payload) => {
    return {
        type : FETCH_SKILL_PAGE_BANNER,
        payload
    }
}

export {
    fetchSkillPageBanner,
}