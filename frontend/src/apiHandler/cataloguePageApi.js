import { fetchRecentlyAddedCourses, fetchPopularServices, 
    fetchAllCategoriesAndVendors, fetchTrendingCategories } from 'store/CataloguePage/actions/index';


export const getCataloguePageActions = () => {
    return [
        { action : fetchRecentlyAddedCourses, payload : {}},
        { action : fetchPopularServices, payload : {}},
        { action : fetchAllCategoriesAndVendors, payload : {num: 8}},
        { action : fetchTrendingCategories, payload: { 'medium': 0}},
    ]
}

export const getCataloguePageActionsMobile = () => {
    return [
        { action : fetchRecentlyAddedCourses, payload : {}},
        { action : fetchPopularServices, payload : {}},
        { action : fetchAllCategoriesAndVendors, payload : {num: 8}},
        { action : fetchTrendingCategories, payload: { 'medium': 1}},
    ]
}