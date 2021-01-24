import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './myWallet.scss';
import { fetchMyWallet } from 'store/DashboardPage/MyWallet/actions/index';
import { startDashboardWalletPageLoader, stopDashboardWalletPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import Pagination from '../../../Common/Pagination/pagination';

   
const MyWallet = (props) => {
    const { loyality_txns, page, wal_total } = useSelector(store => store.dashboardWallet?.data)
    const { walletLoader } = useSelector(store => store.loader);
    const [showModal, setShowModal] = useState(false)
    const [currentPage, setCurrentPage] = useState(1)
    const dispatch = useDispatch();

    const handleEffects = async () => {
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardWalletPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyWallet({ page: currentPage, resolve, reject })))
                dispatch(stopDashboardWalletPageLoader());
            }
            else {
                delete window.config?.isServerRendered
            }
        } catch (error) {
            // if (error?.status == 404) {
            //     history.push('/404');
            // }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [currentPage])

    return(
        <>
            { walletLoader && <Loader />}
            <div className="m-wallet db-warp">
                <div className="m-card">
                    <div className="m-wallet__firstCard">
                        <div className="m-wallet__firstCard--rhs">
                            <span>Loyality point balance</span>
                            <h2> { wal_total?.toFixed(2) } </h2>
                        </div>

                        <button className="btn-blue-outline btn-xs" onClick={() => setShowModal(true)}>Redeem now</button>
                    </div>
                </div>

                {
                    loyality_txns?.map((txn, index) => {
                        return (
                            <div className="m-card" key={ index }>
                                <span className="m-wallet--date">{ txn?.date }</span>
                                <ul className="m-wallet--info">
                                    <li className="head">{ txn?.order_id }</li>
                                    <li className= { txn?.txn_sign === '+' ? 'lPoints text-green' :  'lPoints text-red' }>{ txn?.txn_sign }{ txn?.loyality_points?.toFixed(2) }</li>
                                    <li className="blance">{ txn?.balance?.toFixed(2) }</li>
                                </ul>

                                <div className="m-pipe-divides">
                                    <span>{ txn?.get_txn_type }</span>
                                    <span>Expiry date: <strong>{ txn?.expiry_date }</strong></span>
                                </div>
                            </div>
                        )
                    })
                }
                
                {/* <div className="m-card">
                    <span className="m-wallet--date">27 Oct 2020</span>
                    <ul className="m-wallet--info">
                        <li className="head">CT2456912</li>
                        <li className="lPoints text-red">-47.00</li>
                        <li className="blance">47.00</li>
                    </ul>

                    <div className="m-pipe-divides">
                        <span>Expierd</span>
                        <span>Expiry date: <strong>27 Oct 2020</strong></span>
                    </div>
                </div>
                
                <div className="m-card">
                    <span className="m-wallet--date">27 Oct 2020</span>
                    <ul className="m-wallet--info">
                        <li className="head">CT2456912</li>
                        <li className="lPoints text-green">-470.00</li>
                        <li className="blance">450.00</li>
                    </ul>

                    <div className="m-pipe-divides">
                        <span>Added</span>
                        <span>Expiry date: <strong>27 Oct 2020</strong></span>
                    </div>
                </div>
                
                <div className="m-card">
                    <span className="m-wallet--date">27 Oct 2020</span>
                    <ul className="m-wallet--info">
                        <li className="head">CT2456912</li>
                        <li className="lPoints text-green">+437.00</li>
                        <li className="blance">389.00</li>
                    </ul>

                    <div className="m-pipe-divides">
                        <span>Reverted</span>
                        <span>Expiry date: <strong>27 Oct 2020</strong></span>
                    </div>
                </div>
                
                <div className="m-card">
                    <span className="m-wallet--date">27 Oct 2020</span>
                    <ul className="m-wallet--info">
                        <li className="head">CT2456912</li>
                        <li className="lPoints text-red">-47.00</li>
                        <li className="blance">47.00</li>
                    </ul>

                    <div className="m-pipe-divides">
                        <span>Reedemed</span>
                        <span>Expiry date: <strong>27 Oct 2020</strong></span>
                    </div>
                </div> */}

                { 
                    showModal &&
                        <div className="m-slide-modal">
                            <div className="text-center redeem-now">
                                    <span className="m-db-close" onClick={() => setShowModal(false)}>&#x2715;</span>
                                    <i className="redeem-now--icon"></i>
                                    <h2>Congratulations!</h2>
                                    <p>
                                        <strong className="redeem-now--lPoints d-block">{ wal_total?.toFixed(2) }</strong>
                                        loyality point is reedemed and added <br/>in your wallet
                                    </p>
                                    <a href="/payment/payment-summary" className="font-weight-bold">Ok</a>
                            </div>
                        </div>
                }
                <br />
                {
                    page?.total > 1 ? <Pagination totalPage={page?.total_page} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''
                }
            </div>
        </>
    )
}
   
export default MyWallet;