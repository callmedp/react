import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'
import { useSelector } from 'react-redux';

const CTA = (props) => {
    const { setEnquiryForm } = props
    const { callUs } = useSelector(store => store.header)
    
    const showEnquiryForm = (event) => {
        event.preventDefault();
        setEnquiryForm(true)
    }

    // const zendeskChat = () => {
    //     window.$zopim(function () {
    //         window.$zopim.livechat.window.show();
    //         window.$zopim.livechat.window.onHide(function () {
    //             window.$zopim.livechat.hideAll()
    //         })
    //     });
    // }

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
            <a href="#" onClick={(e) => {e.preventDefault();}}>
                <figure className="micon-chat"></figure>
                Chat
            </a>
            <Link to={"#"}>
                <figure className="micon-whatsapp"></figure>
                Whatsapp
            </Link>
        </section>
    )
}

export default CTA;