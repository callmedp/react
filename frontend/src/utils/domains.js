// Please don't change any variable directy in here. If you wan't to change it, do with in the .env file.
// For info on how to use .env file visit https://create-react-app.dev/docs/adding-custom-environment-variables/

export const siteDomain =  window?.config?.siteDomain  || process.env.REACT_APP_SITE_DOMAIN || 'https://learning.shine.com';

export const resumeShineSiteDomain = window?.config?.resumeShineSiteDomain || process.env.REACT_APP_RESUME_SHINE_SITE_DOMAIN ||  'https://resume.shine.com';

export const imageUrl = window?.config?.imageUrl ||  process.env.REACT_APP_IMAGE_URL || '/media/static/react/media/images/';

export const shineSiteDomain = window?.config?.shineSiteDomain || process.env.REACT_APP_SHINE_SITE_DOMAIN || 'https://mapi.shine.com';

export const shineDomain = 'https://www.shine.com';

export const shineSiteUrl = 'https://www.shine.com/jobs/';

export const chatbotDomain = window?.config?.chatbotDomain || process.env.REACT_APP_CHATBOT_SITE_DOMAIN ||  'https://chat.shine.com';

export const trackingSiteDomain = window?.config?.trackingSiteDomain || process.env.REACT_APP_TRACKING_SITE_DOMAIN ||  'http://34.93.108.100:80/api/v1/core/track';
