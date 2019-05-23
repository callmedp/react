import {
    FETCH_TEMPLATE,
    SET_SELECTED_TEMPLATE,
    CUSTOMIZE_TEMPLATE,
    FETCH_TEMPLATE_IMAGES,
    FETCH_DEFAULT_CUSTOMIZATION
} from './actionTypes'


export const fetchTemplate = (payload) => {
    return {
        type: FETCH_TEMPLATE,
        payload
    }
}

export const displaySelectedTemplate = (templateId) => {
    return {
        type: SET_SELECTED_TEMPLATE,
        templateId
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
