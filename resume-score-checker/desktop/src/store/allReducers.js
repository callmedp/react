import { combineReducers } from 'redux'
import { landingPageReducer } from './LandingPage/reducers/index'
import {googleAnalyticsReducer} from './googleAnalytics/reducer/index'

const allReducer = combineReducers ({
    home : landingPageReducer,
    analytics: googleAnalyticsReducer
})


export default allReducer;