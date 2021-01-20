import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './myWallet.scss';
import { fetchMyWallet } from 'store/DashboardPage/MyWallet/actions/index';
import { startDashboardWalletPageLoader, stopDashboardWalletPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

   
const MyWallet = (props) => {
    const ordPageNo = '1';
    const loyalityTxn = useSelector(store => store.dashboardWallet?.data)
    const { walletLoader } = useSelector(store => store.loader);
    const dispatch = useDispatch();

    const handleEffects = async () => {
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardWalletPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyWallet({ page: 1, resolve, reject })))
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
    }, [ordPageNo])

    return(
        <>
            { walletLoader && <Loader />}
            <div className="m-wallet db-warp">
                <div className="m-card">
                    <div className="m-wallet__firstCard">
                        <div className="m-wallet__firstCard--rhs">
                            <span>Loyality point balance</span>
                            <h2> { loyalityTxn?.wal_total?.toFixed(2) } </h2>
                        </div>

                        <button className="btn-blue-outline btn-xs">Redeem now</button>
                    </div>
                </div>

                {
                    loyalityTxn?.loyality_txns?.map((txn) => {
                        return (
                            <div className="m-card" key={ txn?.order_id }>
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

                {/* <div className="m-slide-modal">
                <div className="text-center redeem-now">
                        <span className="m-db-close">&#x2715;</span>
                        <i className="redeem-now--icon"></i>
                        <h2>Congratulations!</h2>
                        <p>
                            <strong className="redeem-now--lPoints d-block">248.00</strong>
                            loyality point is reedemed and added <br/>in your wallet
                        </p>
                        <Link to={'#'} className="font-weight-bold">Ok</Link>
                </div>
                </div> */}
            </div>
        </>
    )
}
   
export default MyWallet;