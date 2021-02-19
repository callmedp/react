import {
    fetchRecentlyAddedCourses, fetchPopularServices,
    fetchAllCategoriesAndVendors, fetchTrendingCategories
} from 'store/CataloguePage/actions/index';
import { CountryCode2 } from 'utils/storage';
import {sessionAvailability} from 'store/Header/actions/index'

const code2 = CountryCode2()

export const getCataloguePageActions = () => {
    return [
        { action: sessionAvailability, payload: {}},
        { action: fetchRecentlyAddedCourses, payload: { code2: code2 } },
        { action: fetchPopularServices, payload: { code2: code2 } },
        { action: fetchAllCategoriesAndVendors, payload: { num: 8 } },
        { action: fetchTrendingCategories, payload: { 'medium': 0 } },
    ]
}

export const getCataloguePageActionsMobile = () => {
    return [
        { action: sessionAvailability, payload: {}},
        { action: fetchRecentlyAddedCourses, payload: { code2: code2 } },
        { action: fetchPopularServices, payload: { code2: code2 } },
        { action: fetchAllCategoriesAndVendors, payload: { num: 8 } },
        { action: fetchTrendingCategories, payload: { 'medium': 1 } },
    ]
}