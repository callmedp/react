import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Swal from 'sweetalert2';
import './myOrders.scss';
import { useDispatch, useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { downloadInvoice } from 'utils/dashboardUtils/myOrderUtils';
import { fetchMyOrders, cancelOrder } from 'store/DashboardPage/MyOrder/actions/index';
import { startDashboardOrderPageLoader, stopDashboardOrderPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import Pagination from '../../../Common/Pagination/pagination';
import { getDataStorage } from 'utils/storage';

   
const MyWallet = (props) => {
    const dispatch = useDispatch();
    const [currentPage, setCurrentPage] = useState(1)
    const { data, page } = useSelector(store => store.dashboardOrders)
    const { orderLoader } = useSelector(store => store.loader);
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const [showCancelModal, setShowCancelModal] = useState(false)
    const [cancelOrderId, setCancelOrderId] = useState('')

    const handleEffects = async () => {
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardOrderPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyOrders({ page: currentPage, resolve, reject })))
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
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
        handleEffects();
    }, [currentPage])

    const showDetails = (id) => {
        id == showOrderDetailsID ?
            setShowOrderDetailsID('') : setShowOrderDetailsID(id)
    }

    const handleCancellation = async (orderId) => {
        setShowCancelModal(false)
        dispatch(startDashboardOrderPageLoader());
        var result = await new Promise((resolve, reject) => dispatch( 
            cancelOrder({
                payload: {
                    order_id: orderId,
                    // candidate_id: getDataStorage('candidate_id'),
                    // email: getDataStorage('email')
                }, resolve, reject
            })
        ));
        if (result.cancelled) {
            Swal.fire({
                // html: result,
                title: result.data,
                icon: 'success'
            })
            handleEffects();
            dispatch(stopDashboardOrderPageLoader());
        }
        else {
            Swal.fire({
                // html: result,
                title: result.error,
                icon: 'error'
            })
            dispatch(stopDashboardOrderPageLoader());
        }
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
                                    { order?.order?.canCancel && <a href='/' onClick={(e) => {e.preventDefault();setShowCancelModal(true);setCancelOrderId(order?.order?.id)}}>Cancel order</a> }
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
            </div> 

            {
                page?.total > 1 ? <Pagination totalPage={page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''
            }

            { 
                showCancelModal &&  
                    <div className="m-slide-modal text-center">
                        <h2 className="mt-15">Do you wish to cancel the order?</h2>
                        <div className="m-enquire-now mt-15 text-center">
                            <div className="m-form-group">
                                <p>Any credit points reedemed against this order will be refunded back to your wallet shortly. These points will be valid for next 10 days. </p>
                            </div>
                            <button className="btn btn-blue" onClick={() => handleCancellation(cancelOrderId)}>Yes</button> 
                            <button className="btn btn-blue-outline ml-10" onClick={() => {setShowCancelModal(false)}}>No</button>
                        </div>
                    </div>
            }
        </>
    )
}
   
export default MyWallet;