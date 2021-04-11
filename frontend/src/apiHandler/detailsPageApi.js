import {
    fetchMainCourses,
    fetchProductReviews,
} from 'store/DetailPage/actions';

export const getDetailPageActions = (params) => {
    return [
        { action: fetchMainCourses, payload: { id: params?.id, device:'desktop'}},
        { action: fetchProductReviews, payload: { prdId: 1, page: 1, device: 'desktop' } },
    ]
}

export const getDetailPageActionsMobile = (params) => {
    return [
        { action: fetchMainCourses, payload: { id: params?.id, device:'mobile'}},
        { action: fetchProductReviews, payload: { prdId: 1, page: 1, device: 'mobile' } },
    ]
}