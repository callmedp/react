import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Table from 'react-bootstrap/Table'
import { fetchShoppingList } from 'store/HomePage/actions'

const Homepage = () => {
    console.log("homepage container")
    const dispatch = useDispatch()

    const { shoppingList } = useSelector(state => state.home)
    console.log("shopping list", shoppingList)
    useEffect(() => {
        // dispatch(fetchShoppingList({}))
        new Promise((resolve, reject) => dispatch(fetchShoppingList({ payload: {}, resolve, reject })))
    }, [])

    return (
        <Table striped bordered hover variant="dark">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Shopping Site</th>
                    <th>Username</th>
                </tr>
            </thead>
            <tbody>
               
                {
                    shoppingList?.map((site) => {
                        return (
                            <tr>
                            <td>{site.id}</td>
                            <td>{site.name}</td>
                            <td>{site.username}</td>
                        </tr>
                        )
                    })
                }
            </tbody>
        </Table>
    )
}




export default Homepage;
