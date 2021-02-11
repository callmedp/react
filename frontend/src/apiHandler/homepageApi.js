import {
    fetchMostViewedCourses,
    fetchInDemandProducts,
    fetchJobAssistanceAndBlogs,
    fetchTestimonials,
} from 'store/HomePage/actions';


export const getHomepageActions = () => {
    return [
        { action: fetchMostViewedCourses, payload: { categoryId: -1} },
        { action: fetchInDemandProducts, payload: { pageId: 1, tabType: 'master', device:'desktop'}},
        { action: fetchJobAssistanceAndBlogs, payload: { } },
        { action: fetchTestimonials, payload: { device : 'desktop' } },
    ]
}

export const getHomepageActionsMobile = () => {
    return [
        { action: fetchMostViewedCourses, payload: { categoryId: -1} },
        { action: fetchInDemandProducts, payload: { pageId: 1, tabType: 'master', device:'mobile'}},
        { action: fetchJobAssistanceAndBlogs, payload: { } },
        { action: fetchTestimonials, payload: { device : 'mobile' } },
    ]
}