import {
    shoppingListFetched
} from './actions';

const shoppingListState = {
    shoppingList: []
}

export const HomepageReducer = (state = shoppingListState, action) => {
    switch (action.type) {
        case shoppingListFetched.type: return { shoppingList: action.payload.item }
        default: return state;
    }
}
