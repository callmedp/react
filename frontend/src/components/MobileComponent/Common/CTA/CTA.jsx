import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'
import { useSelector } from 'react-redux';
import { zendeskChatShow } from 'utils/zendeskIniti';

const CTA = (props) => {
    const { setEnquiryForm, pageType, heading } = props
    const { callUs, prd_course_number, prd_service_number,
    course_skill_number, service_skill_number } = useSelector(store => store.header)
    
    const showEnquiryForm = (event) => {
        event.preventDefault();
        setEnquiryForm(true)
    }

    if(pageType === 'skill'){
        var whatsappNo = course_skill_number
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