import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'

const CTA = (props) => {
    const { setEnquiryForm } = props
    
    const showEnquiryForm = (event) => {
        event.preventDefault();
        setEnquiryForm(true)
    }
    return(
        <section className="m-container m-cta">
            <a href="#" onClick={showEnquiryForm}>
                <figure className="micon-enquiry"></figure>
                Enquiry
            </a>
            <Link to={"#"}>
                <figure className="micon-callus"></figure>
                Call us
            </Link>
            <Link to={"#"}>
                <figure className="micon-chat"></figure>
                Chat
            </Link>
            <Link to={"#"}>
                <figure className="micon-whatsapp"></figure>
                Whatsapp
            </Link>
        </section>
    )
}

export default CTA;