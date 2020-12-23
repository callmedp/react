import React, { useState, useEffect }from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'
import { useSelector } from 'react-redux';
import { zendeskChatShow } from 'utils/zendeskIniti';
import { getWhatsAppNo } from 'utils/whatsappNo';

const CTA = (props) => {
    const { setEnquiryForm, pageType, heading } = props
    const { callUs, whatsappDict } = useSelector(store => store.header)
    const [whatsappNo, setWhatsAppNo] = useState('')
    
    const showEnquiryForm = (event) => {
        event.preventDefault();
        setEnquiryForm(true)
    }

    useEffect(()=>{
        setWhatsAppNo(getWhatsAppNo(pageType, whatsappDict))
    }, [whatsappDict])

    return(
        <section className="m-container m-cta" data-aos="fade-up">
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
            { whatsappNo ?
                <a href={`https://api.whatsapp.com/send?phone=91${whatsappNo}&text=I need your help for ${heading}`}>
                    <figure className="micon-whatsapp"></figure>
                    Whatsapp
                </a> : null
            }
        </section>
    )
}

export default CTA;