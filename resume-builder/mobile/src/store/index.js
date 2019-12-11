import {createStore, applyMiddleware, compose} from 'redux';
import reducer from './allReducers'
import rootSaga from './sagas'
import createSagaMiddleware from 'redux-saga';
import {composeWithDevTools} from 'redux-devtools-extension';
import {createMiddleware} from 'redux-beacon';
import GoogleAnalytics from '@redux-beacon/google-analytics';
import {eventsMap} from './googleAnalayticsEventMap';

const ga = GoogleAnalytics();
const google_analytics_middleware = createMiddleware(eventsMap, ga)
const sagaMiddleware = createSagaMiddleware();

const composeEnhancers = (typeof window !== 'undefined') && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;


// Grab the state from a global variable injected into the server-generated HTML
const preloadedState = window.__PRELOADED_STATE__

// Allow the passed state to be garbage-collected
delete window.__PRELOADED_STATE__

const store = createStore(reducer, preloadedState, composeEnhancers(
    applyMiddleware(sagaMiddleware, google_analytics_middleware)));

sagaMiddleware.run(rootSaga);


export default store;