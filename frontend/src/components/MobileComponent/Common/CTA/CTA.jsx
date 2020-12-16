import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'
import { useSelector } from 'react-redux';
import { zendeskChatShow } from 'utils/zendeskIniti';

const CTA = (props) => {
    const { setEnquiryForm } = props
    const { callUs } = useSelector(store => store.header)
    
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
            <a href={`tel:${callUs}`}>
                <figure className="micon-callus"></figure>
                Call us
            </a>
            <a href="#" onClick={(e) => {e.preventDefault();zendeskChatShow();}}>
                <figure className="micon-chat"></figure>
                Chat
            </a>
            {/* <Link to={"#"}>
                <figure className="micon-whatsapp"></figure>
                Whatsapp
            </Link> */}
        </section>
    )
}

export default CTA;