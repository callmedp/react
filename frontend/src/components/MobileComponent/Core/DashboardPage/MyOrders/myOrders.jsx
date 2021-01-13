import React from 'react';
import { Link } from 'react-router-dom';
import './myOrders.scss';

   
const MyWallet = (props) => {
    return(
        <div className="my-order db-warp mb-20">

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
            </div>


        </div>
    )
}
   
export default MyWallet;