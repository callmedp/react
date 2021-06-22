import React, { useState, useEffect }from 'react';
import './cta.scss'
import { useSelector } from 'react-redux';
import { zendeskChatShow } from 'utils/zendeskIniti';
import { getWhatsAppNo } from 'utils/whatsappNo';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const CTA = (props) => {
    const { setEnquiryForm, pageType, heading, contact } = props
    const { callUs, whatsappDict } = useSelector(store => store.header)
    const [whatsappNo, setWhatsAppNo] = useState('')
    const sendLearningTracking = useLearningTracking();

    const showEnquiryForm = (event) => {
        event.preventDefault();
        setEnquiryForm(true);

        sendLearningTracking({
            productId: '',
            event: `${pageType}_${stringReplace(heading)}_enquire_now_clicked`,
            pageTitle: pageType,
            sectionPlacement: 'CTA',
            eventCategory: ``,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const callUsTracking = () => {
        sendLearningTracking({
            productId: '',
            event: `${pageType}_${stringReplace(heading)}_${contact}_call_us_clicked`,
            pageTitle: pageType,
            sectionPlacement: 'CTA',
            eventCategory: ``,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const showChatbot = () => {
        if(window) {
            window.openChat();
            sendLearningTracking({
                productId: '',
                event: `${pageType}_${stringReplace(heading)}_shiney_chat_clicked`,
                pageTitle: pageType,
                sectionPlacement: 'CTA',
                eventCategory: ``,
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: '',
            })
        }
    }

    const handleScroll = () =>{
        if(window) {
            const offset = window.scrollY;
            if(offset === 0) window.openChat();
        }
    }

    useEffect(()=>{
        setWhatsAppNo(getWhatsAppNo(pageType, whatsappDict));
        window.addEventListener('scroll', handleScroll);
    }, [whatsappDict])

    return(
        <section className="m-container m-cta" data-aos="fade-up">
            <a href="#" onClick={showEnquiryForm}>
                <figure className="micon-enquiry"></figure>
                Enquiry
            </a>
            <a href={!!contact ? `tel:${contact}` : `tel:${callUs}`} onClick={callUsTracking}>
                <figure className="micon-callus"></figure>
                Call us
            </a>
            { whatsappNo ?
                <a href={`https://api.whatsapp.com/send?phone=91${whatsappNo}&text=I need your help for ${heading}`}>
                    <figure className="micon-whatsapp"></figure>
                    Whatsapp
                </a> : null
            }
            <a href="#" onClick={pageType == 'detailPage' ? showChatbot : (e) => {e.preventDefault();zendeskChatShow();}}>
                <figure className="micon-chat"></figure>
                Chat
            </a>
        </section>
    )
}

export default CTA;