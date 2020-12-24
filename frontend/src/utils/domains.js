// Please don't change any variable directy in here. If you wan't to change it, do with in the .env file.
// For info on how to use .env file visit https://create-react-app.dev/docs/adding-custom-environment-variables/

export const siteDomain =  window?.config?.siteDomain  || process.env.REACT_APP_SITE_DOMAIN || 'https://learning.shine.com';

export const resumeShineSiteDomain = window?.config?.resumeShineSiteDomain || process.env.REACT_APP_RESUME_SHINE_SITE_DOMAIN ||  'https://resume.shine.com';

export const imageUrl = window?.config?.imageUrl ||  process.env.REACT_APP_IMAGE_URL || '/media/static/react/media/images/';