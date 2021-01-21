import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';
import { useDispatch, useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { downloadInvoice } from 'utils/dashboardUtils/myOrderUtils';
import { fetchMyOrders } from 'store/DashboardPage/MyOrder/actions/index';
import { startDashboardOrderPageLoader, stopDashboardOrderPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

   
const MyWallet = (props) => {
    const dispatch = useDispatch();
    const [ordPageNo, setOrdPageNo] = useState(1)
    const { data, page } = useSelector(store => store.dashboardOrders)
    const { orderLoader } = useSelector(store => store.loader);
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')

    const handleEffects = async () => {
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardOrderPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyOrders({ page: ordPageNo, resolve, reject })))
                dispatch(stopDashboardOrderPageLoader());
            }
            else {
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
            }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [ordPageNo])

    const showDetails = (id) => {
        id == showOrderDetailsID ?
            setShowOrderDetailsID('') : setShowOrderDetailsID(id)
    }

    const getOrderDetails = (orderItems) => {
        return (
            <>
                {
                    orderItems?.map((oi) => {
                        return(
                            <ul className="my-order__order-detail--info mt-15" key={oi?.id}>
                                <li>
                                    <a href={`${siteDomain}${oi?.productUrl}`} className="d-block mb-0">{oi?.name} </a>
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
        <>
            { orderLoader && <Loader /> }
            <div className="my-order db-warp mb-20">
                {
                    data?.map((order, index) => {
                        return (
                            <div className="m-card" key={ index }>
                                <p className="head mb-5">{order?.order?.number}</p>

                                <div className="m-pipe-divides">
                                    <span>Placed on: <strong>{order?.order?.date_placed}</strong></span>
                                    <span>Status: <strong>{order?.order?.status}</strong></span>
                                    <span><strong>{order?.item_count}</strong> {order?.item_count > 1 ? 'items' : 'item'}</span>
                                </div>

                                <div className="my-order--wrap mt-20">
                                    <div className="my-order__priceWrap">
                                        <span className="my-order__priceWrap--tAmount d-block">Total amount</span>
                                        <strong className="my-order__priceWrap--price">{ order?.order?.currency === 'Rs.' ? <span>&#8377;</span> : order?.order?.currency } {order?.order?.total_incl_tax}/- </strong>
                                    </div>
                                    { order?.order?.canCancel && <Link to={"#"}>Cancel order</Link> }
                                    { order?.order?.downloadInvoice && <a href={downloadInvoice(order?.order?.id)} target="_blank">Download Invoice</a> }
                                    
                                </div>

                                <div className="my-order__order-detail">
                                    <Link to={"#"} onClick={() => showDetails(order?.order?.id)} className={(showOrderDetailsID === order?.order?.id) ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"}>Order Details</Link>
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
            <span onClick={()=>setOrdPageNo(ordPageNo + 1)}>&emsp; &emsp; &emsp;{ ordPageNo }</span>
        </>
    )
}
   
export default MyWallet;