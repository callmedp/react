import {
    fetchMainCourses,
    fetchProductReviews,
} from 'store/DetailPage/actions';

export const getDetailPageActions = () => {
    return [
        { action: fetchMainCourses, payload: { id: 1, device:'desktop'}},
        { action: fetchProductReviews, payload: { prdId: 1, page: 1, device: 'desktop' } },
    ]
}

export const getDetailPageActionsMobile = () => {
    return [
        { action: fetchMainCourses, payload: { id: 1, device:'mobile'}},
        { action: fetchProductReviews, payload: { prdId: 1, page: 1, device: 'mobile' } },
    ]
}