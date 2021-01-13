import React from 'react';
import { Link } from 'react-router-dom';
import './myWallet.scss';

   
const MyWallet = (props) => {
    return(
        <div className="m-wallet db-warp">
            <div className="m-card">
                <div className="m-wallet__firstCard">
                    <div className="m-wallet__firstCard--rhs">
                        <span>Loyality point balance</span>
                        <h2>248.00 </h2>
                    </div>

                    <button className="btn-blue-outline btn-xs">Redeem now</button>
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
            </div>

            <div className="m-slide-modal">
               <div className="text-center redeem-now">
                    <span className="m-db-close">&#x2715;</span>
                    <i className="redeem-now--icon"></i>
                    <h2>Congratulations!</h2>
                    <p>
                        <strong className="redeem-now--lPoints d-block">248.00</strong>
                        loyality point is reedemed and added <br/>in your wallet
                    </p>
                    <Link className="font-weight-bold">Ok</Link>
               </div>
            </div>
        </div>
    )
}
   
export default MyWallet;