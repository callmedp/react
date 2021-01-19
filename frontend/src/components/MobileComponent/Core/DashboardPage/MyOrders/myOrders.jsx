import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';
import { useDispatch, useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { downloadInvoice } from 'utils/dashboardUtils/myOrderUtils';

   
const MyWallet = (props) => {
    const ordersList = useSelector(store => store.dashboardOrders?.data)
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')

    const getOrderStatus = (key) => {
        return (
            (key === 1 && "Open") || (key === 0 && "Unpaid") || 
            (key === 3 && "Closed") || (key === 5 && "Cancelled")
        )
    }

    const getOrderDetails = (orderItems) => {
        return (
            <>
                {
                    orderItems?.map((oi) => {
                        return(
                            <ul className="my-order__order-detail--info mt-15" key={oi?.id}>
                                <li>
                                    <a href={`${siteDomain}${oi?.productUrl}`} className="d-block mb-0">{oi?.title} </a>
                                    <span> Status: <strong>{oi?.oi_status}</strong></span>
                                </li>
                            </ul>
                        )
                    })
                }
            </>
        )
    }

    return(
        <div className="my-order db-warp mb-20">
            {
                ordersList?.map((order) => {
                    return (
                        <div className="m-card" key={order?.order?.number}>
                            <p className="head mb-5">{order?.order?.number}</p>

                            <div className="m-pipe-divides">
                                <span>Placed on: <strong>{order?.order?.date_placed}</strong></span>
                                <span>Status: <strong>{getOrderStatus(order?.order?.status)}</strong></span>
                                <span>Status: <strong>{order?.item_count}</strong> {order?.item_count > 1 ? 'items' : 'item'}</span>
                            </div>

                            <div className="my-order--wrap mt-20">
                                <div className="my-order__priceWrap">
                                    <span className="my-order__priceWrap--tAmount d-block">Total amount</span>
                                    <strong className="my-order__priceWrap--price">{ order?.order?.currency === 'Rs.' ? <span>&#8377;</span> : order?.order?.currency } {order?.order?.total_incl_tax}/- </strong>
                                </div>
                                {
                                    order?.order?.status === 0 ? <Link to={"#"}>Cancel order</Link> : 
                                        (order?.order?.status === 1 || order?.order?.status === 3) ? <a href={downloadInvoice(order?.order?.id)} target="_blank">Download Invoice</a> : ''
                                }
                                
                            </div>

                            <div className="my-order__order-detail">
                                <Link to={"#"} onClick={() => setShowOrderDetailsID(order?.order?.id)} className={(showOrderDetailsID === order?.order?.id) ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"}>Order Details</Link>
                                { (showOrderDetailsID === order?.order?.id) && getOrderDetails(order?.orderitems) }
                            </div>
                        </div>
                    )
                })
            }
            {/* <div className="m-card">
                <p className="head mb-5">CP279912</p>

                <div className="m-pipe-divides">
                    <span>Placed on: <strong>27 Oct 2020</strong></span>
                    <span>Status: <strong>Open</strong></span>
                    <span>Status: <strong>2</strong> items</span>
                </div>

                <div className="my-order--wrap mt-20">
                    <div className="my-order__priceWrap">
                        <span className="my-order__priceWrap--tAmount d-block">Total amount</span>
                        <strong className="my-order__priceWrap--price">&#8377; 19922/- </strong>
                    </div>

                    <Link to={"#"}>Download Invoice</Link>
                </div>

                <div className="my-order__order-detail">
                    <Link to={"#"} className="font-weight-bold arrow-icon">Order Details</Link>
                </div>
            </div>
            
            <div className="m-card">
                <p className="head mb-5">CP279912</p>

                <div className="m-pipe-divides">
                    <span>Placed on: <strong>27 Oct 2020</strong></span>
                    <span>Status: <strong>Open</strong></span>
                    <span>Status: <strong>2</strong> items</span>
                </div>

                <div className="my-order--wrap mt-20">
                    <div className="my-order__priceWrap">
                        <span className="my-order__priceWrap--tAmount d-block">Total amount</span>
                        <strong className="my-order__priceWrap--price">&#8377; 19922/- </strong>
                    </div>

                    <Link to={"#"}>Download Invoice</Link>
                </div>

                <div className="my-order__order-detail">
                    <Link to={"#"} className="arrow-icon open font-weight-bold">Order Details</Link>

                    <ul className="my-order__order-detail--info mt-15">
                        <li>
                            <Link to={"#"} className="d-block mb-0">Prince2 Foundation Training </Link>
                            <span> Status: <strong>In progress</strong></span>
                        </li>
                        <li>
                            <Link to={"#"} className="d-block mb-0">Resume Builder - 14 days @ Rs 199 Unpaid</Link>
                            <span> Status: <strong>In progress</strong></span>
                        </li>
                    </ul>
                </div>
            </div>

            <div className="m-card">
                <p className="head mb-5">CP279912</p>

                <div className="m-pipe-divides">
                    <span>Placed on: <strong>27 Oct 2020</strong></span>
                    <span>Status: <strong>Open</strong></span>
                    <span>Status: <strong>2</strong> items</span>
                </div>

                <div className="my-order--wrap mt-20">
                    <div className="my-order__priceWrap">
                        <span className="my-order__priceWrap--tAmount d-block">Total amount</span>
                        <strong className="my-order__priceWrap--price">&#8377; 19922/- </strong>
                    </div>

                    <Link to={"#"}>Cancel order</Link>
                </div>

                <div className="my-order__order-detail">
                    <Link to={"#"} className="font-weight-bold arrow-icon">Order Details</Link>
                </div>
            </div>*/}


        </div> 
    )
}
   
export default MyWallet;