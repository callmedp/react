import {FETCH_TEMPLATE, SET_SELECTED_TEMPLATE, CUSTOMIZE_TEMPLATE,FETCH_TEMPLATE_IMAGES} from './actionTypes'


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

export const fetchTemplateImages = () => {
    return {
        type: FETCH_TEMPLATE_IMAGES,
    }
}
