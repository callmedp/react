import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import './myWallet.scss';

   
const MyWallet = (props) => {

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);


    return(

        <div className="myWallet">
            <div className="row">
                <div className="col-8 myWallet--heading">
                    Loyality point balance - <strong>248.00</strong>
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
                                <p className="db-redeemnow-popup--points">248.00</p>
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
                <ul className="row myWallet__list">
                    <li className="col-md-2">Oct. 28, 2020</li>
                    <li className="col-md-2">CP24540</li>
                    <li className="col-md-2">Redeemed</li>
                    <li className="col-md-2 text-danger">-312.00</li>
                    <li className="col-md-2">Nov. 27, 2020</li>
                    <li className="col-md-2">390.00</li>
                </ul>
                <ul className="row myWallet__list">
                    <li className="col-md-2">Sept. 01, 2020</li>
                    <li className="col-md-2">CP24540</li>
                    <li className="col-md-2">Expired</li>
                    <li className="col-md-2 text-danger">-312.00</li>
                    <li className="col-md-2">Sept. 27, 2020</li>
                    <li className="col-md-2">460.00</li>
                </ul>

                <ul className="row myWallet__list">
                    <li className="col-md-2">Oct. 28, 2020</li>
                    <li className="col-md-2">CP24540</li>
                    <li className="col-md-2">Reverted</li>
                    <li className="col-md-2 text-success">+312.00</li>
                    <li className="col-md-2">Nov. 28, 2020</li>
                    <li className="col-md-2">390.00</li>
                </ul>
                
                <ul className="row myWallet__list">
                    <li className="col-md-2">Aug. 21, 2020</li>
                    <li className="col-md-2">CP489201</li>
                    <li className="col-md-2">Added</li>
                    <li className="col-md-2 text-success">+590.00</li>
                    <li className="col-md-2">Dec. 27, 2020</li>
                    <li className="col-md-2">210.00</li>
                </ul>

                <ul className="row myWallet__list">
                    <li className="col-md-2">Oct. 28, 2020</li>
                    <li className="col-md-2">DR748210</li>
                    <li className="col-md-2">Expired</li>
                    <li className="col-md-2 text-danger">-390.00</li>
                    <li className="col-md-2">Nov. 28, 2020</li>
                    <li className="col-md-2">390.00</li>
                </ul>
                
                <ul className="row myWallet__list">
                    <li className="col-md-2">Oct. 28, 2020</li>
                    <li className="col-md-2">CP24540</li>
                    <li className="col-md-2">Added</li>
                    <li className="col-md-2 text-success">+312.00</li>
                    <li className="col-md-2">Dec. 30, 2020</li>
                    <li className="col-md-2">390.00</li>
                </ul>
            </div>
        </div>
    )
}
   
export default MyWallet;