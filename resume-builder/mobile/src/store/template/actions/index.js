import {FETCH_TEMPLATE,UPDATE_MODAL_STATUS,CUSTOMIZE_TEMPLATE,FETCH_DEFAULT_CUSTOMIZATION,FETCH_THUMBNAIL_IMAGES,REORDER_SECTION,FETCH_SELECTED_TEMPLATE_IMAGE} from './actionTypes'


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

export const fetchThumbNailImages = () => {
    return {
        type: FETCH_THUMBNAIL_IMAGES,
    }
}

export const fetchSelectedTemplateImage = (payload) => {
    return {
        type: FETCH_SELECTED_TEMPLATE_IMAGE,
        payload
    }
}

export const reorderSection = (payload) => {
    return {
        type: REORDER_SECTION,
        payload
    }
}