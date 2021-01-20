import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';
import { startDashboardOrderPageLoader, stopDashboardOrderPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyOrders } from 'store/DashboardPage/MyOrder/actions';

const MyOrders = (props) => {
    const ordPageNo = '1';
    const dispatch = useDispatch();
    const { history } = props;
    const { orderLoader } = useSelector(store => store.loader);
    const results = useSelector(store => store.dashboardOrders);

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardOrderPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyOrders({ page: ordPageNo, resolve, reject })))
                dispatch(stopDashboardOrderPageLoader());
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [ordPageNo])

    const [ selectedOrderIndex, toggleQuestion ] = useState(0);
  
    function openOrderDetail(index) {
        toggleQuestion(selectedOrderIndex === index ? -1 : index);
    }

    return(
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
                results.data.map((item, index) => {
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
                                    <Link to={'#orderDetails' + index} className="arrow-icon" onClick={() => openOrderDetail(index)}>Order Details</Link>
                                    <Link to={"#"} className="download-icon">{item.order.downloadInvoice ? 'Download Invoice' : item.order.canCancel ? 'Cancel Order' : ""}</Link>
                                </div>
                            </div>

                            {/* dropdown open/close tab */}
                            { selectedOrderIndex === index &&
                                <div id={`orderDetails ${index}`} className="order-detail__content--detail">
                                    {item?.orderitems?.length > 0 ? 
                                        <ul>
                                            <li className="head row">
                                                <span className="col-11 pl-0">Item</span>
                                                <span className="col-1">status</span>
                                            </li>
                                            {
                                                item.orderitems.map((innItem, ind) => {
                                                    return (
                                                        <li className="row" key={ind}>
                                                            <Link to={"#"} className="col-11 pl-0 noLink">
                                                                {innItem.title}
                                                            </Link>
                                                            <span className="col-1 unpaid">{innItem.oi_status}</span>
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
            <h6 className="text-center p-10">Start with your first order and earn loyalty points</h6>
            }
        </div>
    )
}
   
export default MyOrders;