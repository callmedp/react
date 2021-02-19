import {
    fetchMostViewedCourses,
    fetchInDemandProducts,
    fetchJobAssistanceAndBlogs,
    fetchTestimonials,
    fetchSkillwithDemands,
} from 'store/HomePage/actions';
import { sessionAvailability } from 'store/Header/actions/index';

export const getHomepageActions = () => {
    return [
        { action: sessionAvailability, payload: {}},
        { action: fetchMostViewedCourses, payload: { categoryId: -1} },
        { action: fetchInDemandProducts, payload: { pageId: 1, tabType: 'master', device:'desktop'}},
        { action: fetchJobAssistanceAndBlogs, payload: { } },
        { action: fetchTestimonials, payload: { device : 'desktop' } },
    ]
}

export const getHomepageActionsMobile = () => {
    return [
        { action: sessionAvailability, payload: {}},
        { action: fetchMostViewedCourses, payload: { categoryId: -1} },
        { action: fetchInDemandProducts, payload: { pageId: 1, tabType: 'master', device:'mobile'}},
        { action: fetchJobAssistanceAndBlogs, payload: { } },
        { action: fetchTestimonials, payload: { device : 'mobile' } },
        { action: fetchSkillwithDemands, payload: {}},
    ]
}