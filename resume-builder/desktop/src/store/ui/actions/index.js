import {SHOW_TEMPLATE_MODAL,HIDE_TEMPLATE_MODAL} from "./actionTypes";


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