
const fetchShoppingList = (data) => {
    return new Promise((resolve, reject) => resolve([{
        id: 1, name: 'Amazon', username: 'dp123'
    },
    {
        id: 1, name: 'Nykaa', username: 'dp456'
    },
    {
        id: 1, name: 'Flipkart', username: 'dp345'
    },
    {
        id: 1, name: 'Myntra', username: 'dp678'
    }]))
}

export default {
    fetchShoppingList,
}

