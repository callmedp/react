import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';
import { startDashboardOrderPageLoader, stopDashboardOrderPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyOrders, cancelOrder } from 'store/DashboardPage/MyOrder/actions';
import { downloadInvoice } from 'utils/dashboardUtils/myOrderUtils';
import {Toast} from '../../../Common/Toast/toast';
import { Modal } from 'react-bootstrap';
import EmptyInbox from '../Inbox/emptyInbox';
import BreadCrumbs from '../Breadcrumb/Breadcrumb';
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';

const MyOrders = (props) => {
    const ordPageNo = '1';
    const dispatch = useDispatch();
    const { history } = props;
    const { orderLoader } = useSelector(store => store.loader);
    const results = useSelector(store => store.dashboardOrders);
    const [ selectedOrderIndex, toggleQuestion ] = useState(0);
    const [showCancelModal, setShowCancelModal] = useState(false)
    const [cancelOrderId, setCancelOrderId] = useState('')

    const handleEffects = async () => {
        try {
                dispatch(startDashboardOrderPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyOrders({ page: ordPageNo, resolve, reject })))
                dispatch(stopDashboardOrderPageLoader());
        } catch (error) {
            dispatch(stopDashboardOrderPageLoader());
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
    }, [ordPageNo])

  
    function openOrderDetail(index) {
        toggleQuestion(selectedOrderIndex === index ? -1 : index);
    }

    const handleCancellation = async (orderId) => {
        setShowCancelModal(false)
        dispatch(startDashboardOrderPageLoader());
        var result = await new Promise((resolve, reject) => dispatch( 
            cancelOrder({
                payload: {
                    order_id: orderId,
                }, resolve, reject
            })
        ));
        if (result.cancelled) {
            Toast.fire({
                title: result.data,
                icon: 'success'
            })
            handleEffects();
            dispatch(stopDashboardOrderPageLoader());
        }
        else {
            Toast.fire({
                title: result.error,
                icon: 'error'
            })
            dispatch(stopDashboardOrderPageLoader());
        }
    }

    return(
        <div>
            {/* <BreadCrumbs filterStateShow={false} /> */}
            <div className="db-my-order">
            { orderLoader ? <Loader /> : ''}

                <div className="db-white-box">
                    <div className="row">
                        <div className="col-md-4">Order ID</div>
                        <div className="col-md-2">Placed on</div>
                        <div className="col-md-2">Status</div>
                        <div className="col-md-2">No of items</div>
                        <div className="col-md-2">Total Amount</div>
                    </div>
                </div>
                
                {results?.data?.length > 0 ?
                    results?.data?.map((item, index) => {
                        return (
                            <div className="db-white-box order-detail" key={index}>
                                <div className="row">
                                    <div className="col-md-4 order-detail--id">{item.order.number}</div>
                                    <div className="col-md-2 font-weight-bold">{ (new Date(item.order.date_placed)).toLocaleDateString() }</div>
                                    <div className="col-md-2 font-weight-bold">{item.order.status ? item.order.status : ""}</div>
                                    <div className="col-md-2 font-weight-bold">{item.item_count > 1 ? item.item_count + ' items' : item.item_count + ' item'}</div>
                                    <div className="col-md-2 font-weight-bold">{item.order.currency} {item.order.total_incl_tax}/- </div>
                                </div>

                                <div className="order-detail__content">
                                    <div className="order-detail__content--btnWrap">
                                        <Link to={'#orderDetails' + index} className={selectedOrderIndex === index ? "arrow-icon open" : "arrow-icon"} onClick={() => openOrderDetail(index)}>Order Details</Link>
                                        {item.order.downloadInvoice ? <a target="_blank" href={downloadInvoice(item?.order?.id)} className="download-icon">Download Invoice</a> :
                                        item.order.canCancel ? <Link to={"#"} onClick={(e) => {e.preventDefault();setShowCancelModal(true);setCancelOrderId(item?.order?.id); MyGA.SendEvent('DashboardMyOrders','ln_dashboard_left_menu', 'ln_my_orders', 'cancel_order','', false, true);}}>Cancel Order</Link> : null}
                                    </div>
                                </div>

                                {/* dropdown open/close tab */}
                                { selectedOrderIndex === index &&
                                    <div id={`orderDetails ${index}`} className="order-detail__content--detail">
                                        {item?.orderitems?.length > 0 ? 
                                            <ul>
                                                <li className="head row">
                                                    <span className="col-9 pl-0">Item</span>
                                                    <span className="col-3 text-right">Status</span>
                                                </li>
                                                {
                                                    item.orderitems?.map((innItem, ind) => {
                                                        return (
                                                            <li className="row" key={ind}>
                                                                <span className="col-9 pl-0 noLink">
                                                                    {innItem.title}
                                                                </span>
                                                                <span className="col-3 unpaid text-right">{innItem.oi_status}</span>
                                                            </li>
                                                        )
                                                    })
                                                }
                                            </ul>
                                        : ""
                                        }
                                    </div>
                                }
                            </div>
                        )
                    })
                :
                <EmptyInbox inboxButton="Browse Courses" redirectUrl={`${siteDomain}/online-courses.html`} inboxText="You have not ordered any product till now!" />
                }

                {/* cancel order confirmation modal */}
                { 
                    showCancelModal &&  
                    <Modal show={showCancelModal} onHide={setShowCancelModal} className="db-page">
                        <Modal.Header closeButton></Modal.Header>
                        <Modal.Body className="cancel-order">
                        <div className="text-center pl-30 pr-30 pb-3">
                            <h2>Do you wish to cancel the order?</h2>
                            <p className="pb-4">Any credit points reedemed against this order will be refunded back to your wallet shortly. These points will be valid for next 10 days. </p>
                            {/* <strong>Do you wish to cancel the order?</strong>
                            <br />
                            <span>Note: Any credit points reedemed against this order will be refunded back to your wallet shortly. These points will be valid for next 10 days.</span>
                            <br /> <br/> */}

                            <button className="btn btn-outline-primary px-5" onClick={() => handleCancellation(cancelOrderId)}>Yes</button>&emsp;
                            {/* <button className="btn btn-outline-primary px-5" onClick={() => setShowCancelModal(false)}>No</button> */}
                        </div>
                        </Modal.Body>
                    </Modal>
                }
            </div>
        </div>
    )
}
   
export default MyOrders;