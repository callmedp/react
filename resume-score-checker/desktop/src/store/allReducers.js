import { combineReducers } from 'redux'
import { landingPageReducer } from './LandingPage/reducers/index'

const allReducer = combineReducers ({
    home : landingPageReducer,
})


export default allReducer;