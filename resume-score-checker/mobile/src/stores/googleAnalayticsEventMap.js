import { trackPageView, trackEvent }
  from '@redux-beacon/google-analytics';

export const eventsMap = {
    "LOCATION_ROUTE_CHANGE": trackPageView(action => ({
        page: action.payload,
        title: "Route Change"
      })),
    "EVENT_CLICKED": trackEvent(action => {
      return {
        category:'Resume Score Checker',
        action: action.payload.action,
        label: action.payload.label,
      }
    })
};