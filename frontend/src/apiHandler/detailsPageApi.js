import {
    fetchMainCourses,
    fetchReviews,
} from 'store/DetailPage/actions';

export const getDetailPageActions = () => {
    return [
        { action: fetchMainCourses, payload: { pageId: 1, device:'desktop'}},
        { action: fetchReviews, payload: { prdId: 1, page: 1, device: 'desktop' } },
    ]
}

export const getDetailPageActionsMobile = () => {
    console.log(fetchMainCourses);
    return [
        { action: fetchMainCourses, payload: { pageId: 1, device:'mobile'}},
        { action: fetchReviews, payload: { prdId: 1, page: 1, device: 'mobile' } },
    ]
}