import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'

const CTA = (props) => {
    return(
        <section className="m-container m-cta">
            <Link to={"#"}>
                <figure className="micon-enquiry"></figure>
                Enquiry
            </Link>
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