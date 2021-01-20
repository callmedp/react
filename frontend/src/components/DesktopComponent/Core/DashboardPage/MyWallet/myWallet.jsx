import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
// import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import './myWallet.scss';
import { useDispatch, useSelector } from 'react-redux';
import {fetchMyWallet} from 'store/DashboardPage/MyWallet/actions';
import { startDashboardWalletPageLoader, stopDashboardWalletPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const MyWallet = (props) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const walPageNo = '1';
    const dispatch = useDispatch();
    const { history } = props;
    const { walletLoader } = useSelector(store => store.loader);
    const walletResult = useSelector(store => store.dashboardWallet);

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardWalletPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyWallet({ id: walPageNo, resolve, reject })))
                dispatch(stopDashboardWalletPageLoader());
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
    }, [])

    return(
        <div className="myWallet">
           { walletLoader ? <Loader /> : ''}

            <div className="row">
                <div className="col-8 myWallet--heading">
                    Loyality point balance - <strong>{walletResult?.data?.wal_total ? walletResult?.data?.wal_total : 0}</strong>
                    <button 
                        className="btn btn-outline-primary ml-4"
                        onClick={handleShow}
                    >
                        Redeem now
                    </button>

                    <Modal show={show} onHide={handleClose}>
                        <Modal.Header closeButton></Modal.Header>

                        <Modal.Body>
                            <div className="text-center db-redeemnow-popup">
                                <i className="db-green-tick"></i> 
                                <p className="db-redeemnow-popup--heading">Congratulations!</p>
                                <p className="db-redeemnow-popup--points">{walletResult?.data?.wal_total ? walletResult?.data?.wal_total : 0}</p>
                                <p className="db-redeemnow-popup--text">loyality point is reedemed and added <br/>in your wallet</p>
                                <button className="btn btn-link font-weight-bold">Ok</button>
                            </div>
                        </Modal.Body>
                       
                    </Modal>
                </div>
                <div className="col-4 text-right">
                    <Link to={"#"} className="btn btn-link font-weight-bold">FAQs</Link>
                </div>
            </div>

            <div className="db-white-box mt-30">
                <div className="row">
                    <div className="col-md-2">Date</div>
                    <div className="col-md-2">Order id</div>
                    <div className="col-md-2">Description</div>
                    <div className="col-md-2">Loyality points</div>
                    <div className="col-md-2">Expiry date</div>
                    <div className="col-md-2">Balance</div>
                </div>
            </div>

            <div className="db-white-box pb-4">
                {
                    walletResult?.data && walletResult?.data?.loyality_txns.length > 0 ?
                        walletResult?.data?.loyality_txns.map((item, index) => {
                            return (
                                <ul className="row myWallet__list" key={index}>
                                    <li className="col-md-2">{item.date}</li>
                                    <li className="col-md-2">{item.order_id}</li>
                                    <li className="col-md-2">{item.get_txn_type}</li>
                                    <li className={`col-md-2 ${item.txn_sign > '+' ? "text-success" : "text-danger"}`}>{item.txn_sign}{item.loyality_points}</li>
                                    <li className="col-md-2">{item.expiry_date}</li>
                                    <li className="col-md-2">{item.balance}</li>
                                </ul>
                            )
                        })
                    : 
                    <h6 className="text-center p-10">Start with your first order and earn loyalty points</h6>
                }
            </div>
        </div>
    )
}
   
export default MyWallet;