import {LOCATION_ROUTE_CHANGE} from './actionTypes'

export const locationRouteChange = (payload) => {
    return {
        type: LOCATION_ROUTE_CHANGE,
        payload
    }
}