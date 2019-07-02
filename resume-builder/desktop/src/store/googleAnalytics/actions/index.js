import {LOCATION_ROUTE_CHANGE,EVENT_CLICKED} from './actionTypes'

export const locationRouteChange = (payload) => {
    return {
        type: LOCATION_ROUTE_CHANGE,
        payload
    }
}

export const eventClicked = (payload) => {
    return {
        type:EVENT_CLICKED,
        payload
    }
}