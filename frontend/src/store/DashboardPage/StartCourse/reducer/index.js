import * as Actions from '../actions/actionTypes';

const initState = {
    data : {}
}

export const VendorUrlReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.GET_VENDOR_URL : return { ...initState,...action.item};
        default: return state;
    }
}