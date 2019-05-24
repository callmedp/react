import {FETCH_TEMPLATE,UPDATE_MODAL_STATUS,CUSTOMIZE_TEMPLATE,FETCH_DEFAULT_CUSTOMIZATION,FETCH_TEMPLATE_IMAGES} from './actionTypes'


export const fetchTemplate = () => {
    return {
        type: FETCH_TEMPLATE
    }
}

export const updateModalStatus = (payload) => {
    return {
        type: UPDATE_MODAL_STATUS,
        payload
    }
}

export const customizeTemplate = (payload) => {
    return {
        type: CUSTOMIZE_TEMPLATE,
        payload
    }
}

export const fetchDefaultCustomization = (templateId) => {
    return {
        type: FETCH_DEFAULT_CUSTOMIZATION,
        templateId

    }
}

export const fetchTemplateImages = () => {
    return {
        type: FETCH_TEMPLATE_IMAGES,
    }
}