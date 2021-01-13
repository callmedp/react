import React from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';

   
const MyOrders = (props) => {
    return(
        <div className="db-my-order">
            <div className="db-white-box">
                <div className="row">
                    <div className="col-md-4">Order ID</div>
                    <div className="col-md-2">Placed on</div>
                    <div className="col-md-2">Status</div>
                    <div className="col-md-2">No of items</div>
                    <div className="col-md-2">Total Amount</div>
                </div>
            </div>
            
            
            <div className="db-white-box order-detail">
                <div className="row">
                    <div className="col-md-4 order-detail--id">CP279912</div>
                    <div className="col-md-2 font-weight-bold">27 Oct 2020</div>
                    <div className="col-md-2 font-weight-bold">Paid</div>
                    <div className="col-md-2 font-weight-bold">02</div>
                    <div className="col-md-2 font-weight-bold">&#8377; 19922/- </div>
                </div>

                <div className="order-detail__content">
                    <div className="order-detail__content--btnWrap">
                        <Link to={"#orderDetails"} className="arrow-icon">Order Details</Link>
                        <Link className="download-icon">Download Invoice</Link>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box order-detail">
                <div className="row">
                    <div className="col-md-4 order-detail--id">CP279912</div>
                    <div className="col-md-2 font-weight-bold">27 Oct 2020</div>
                    <div className="col-md-2 font-weight-bold">Unpaid</div>
                    <div className="col-md-2 font-weight-bold">02</div>
                    <div className="col-md-2 font-weight-bold">&#8377; 19922/- </div>
                </div>

                <div className="order-detail__content">
                    <div className="order-detail__content--btnWrap">
                        <Link to={"#orderDetails"} className="arrow-icon open">Order Details</Link>
                        <Link>Cancel Order</Link>
                    </div>
                    <div className="order-detail__content--detail">
                        <ul>
                            <li className="head row">
                                <span className="col-11 pl-0">Item</span>
                                <span className="col-1">status</span>
                            </li>
                            <li className="row">
                                <Link to={"#"} className="col-11 pl-0">
                                    Prince2 Foundation Training - Online - 1year-7day
                                </Link>
                                <span className="col-1 unpaid">Paid</span>
                            </li>
                            <li className="row">
                                <Link to={"#"} className="col-11 pl-0">
                                Resume Builder - 14 days @ Rs 199
                                </Link>
                                <span className="col-1 unpaid">Unpaid</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box order-detail">
                <div className="row">
                    <div className="col-md-4 order-detail--id">CP279912</div>
                    <div className="col-md-2 font-weight-bold">27 Oct 2020</div>
                    <div className="col-md-2 font-weight-bold">unpaid</div>
                    <div className="col-md-2 font-weight-bold">02</div>
                    <div className="col-md-2 font-weight-bold">&#8377; 19922/- </div>
                </div>

                <div className="order-detail__content">
                    <div className="order-detail__content--btnWrap">
                        <Link to={"#orderDetails"} className="arrow-icon">Order Details</Link>
                        <Link>Cancel Order</Link>
                    </div>
                </div>
            </div>

        </div>
    )
}
   
export default MyOrders;