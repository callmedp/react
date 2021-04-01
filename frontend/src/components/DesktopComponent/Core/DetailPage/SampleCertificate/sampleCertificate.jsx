import React, {useState} from 'react';
import './sampleCertificate.scss';
import {Link} from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { imageUrl } from 'utils/domains';

const SampleCertificate = (props) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <section className="container-fluid">
            <div className="row">
                <div className="container">
                    <div className="sample-certificate">
                        <h2 className="heading2">Sample certificate</h2>
                        <Link onClick={handleShow} to={"#"}>
                            <figure>
                                <img src={`${imageUrl}/desktop/sample-certificate-thumb.jpg`} alt="Sample certificate" />
                                <span variant="primary">View</span>
                            </figure>
                        </Link>
                    </div>
                    <Modal show={show} 
                        onHide={handleClose}
                        {...props}
                        // size="md"
                        dialogClassName="view-certificate"
                        aria-labelledby="contained-modal-title-vcenter"
                        centered
                    >
                        
                        <Modal.Header closeButton>
                        </Modal.Header>
                        <Modal.Body>
                            <img src={`${imageUrl}/desktop/sample-certificate-big.jpg`} alt="Sample certificate" />
                        </Modal.Body>
                    </Modal>
                </div>
            </div>
        </section>
    )
}


export default SampleCertificate;