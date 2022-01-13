import { createAction } from '@reduxjs/toolkit';

const fetchShoppingList = createAction('FETCH_SHOPPING_LIST');
const shoppingListFetched = createAction('SHOPPING_LIST_FETCHED');


export {
    shoppingListFetched,
    fetchShoppingList
}