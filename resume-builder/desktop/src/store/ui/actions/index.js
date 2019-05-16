import {
    SHOW_TEMPLATE_MODAL,
    HIDE_TEMPLATE_MODAL,
    SHOW_SELECT_TEMPLATE_MODAL,
    HIDE_SELECT_TEMPLATE_MODAL,
    SELECT_CURRENT_FORM
} from "./actionTypes";


export const showModal = () => {
    return {
        type: SHOW_TEMPLATE_MODAL,
        data: {modal: true}
    }
}

export const hideModal = () => {
    return {
        type: HIDE_TEMPLATE_MODAL,
        data: {modal: false}
    }
}

export const showSelectTemplateModal = () => {
    return {
        type: SHOW_SELECT_TEMPLATE_MODAL,
        data: {select_template_modal: true}
    }
}

export const hideSelectTemplateModal = () => {
    return {
        type: HIDE_SELECT_TEMPLATE_MODAL,
        data: {select_template_modal: false}
    }
}

export const currentForm = (payload) => {
    return {
        type: SELECT_CURRENT_FORM,
        data: payload
    }
}