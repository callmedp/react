import React from 'react';
import {Link} from 'react-router-dom';
import Modal from 'react-modal';
import './modals.scss'
 
const CertificateModal = (props) => {
    return(
        <div class="m-container m-certificate-modal m-form-pos-center pb-10" data-aos="zoom-in">
            <div className="m-modal-body">
                <Link to={"#"} className="m-close">x</Link>
                <figure>
                    <img src="/media/images/mobile/sample-certificate-big.jpg" className="img-fluid" alt="Sample certificate" />
                </figure>
            </div>
        </div>
    )
}

export default CertificateModal;