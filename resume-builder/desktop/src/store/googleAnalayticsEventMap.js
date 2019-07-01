import { trackPageView, trackEvent }
  from '@redux-beacon/google-analytics';

export const eventsMap = {
    "LOCATION_ROUTE_CHANGE": trackPageView(action => ({
        page: action.payload,
        title: "Route Change"
      }))
    // "DOWNLOAD_CLICKED": trackEvent()
};