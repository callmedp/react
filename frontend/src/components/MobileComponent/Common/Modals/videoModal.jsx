import React from 'react';
import {  useSelector } from 'react-redux';
import './modals.scss'
import Loader from '../../Common/Loader/loader';

const EnquiryModal = (props) => {
    const { setVideoModal } = props
    const { needHelpLoader } = useSelector(store => store.loader);

    return (
        <>
            {
                needHelpLoader && <Loader />
            }
            <div className="m-container m-enquire-now m-form-pos-btm pb-10" data-aos="fade-up" data-aos-duration="500">
                <span className="m-close" onClick={() => setVideoModal(false)}>x</span>
                <h2 className="m-heading2 text-center"></h2>
                <iframe width="100%" height="280"
                    src="https://www.youtube.com/embed/65CzisMJpJ0?autoplay=1&mute=0&controls=1&modestbranding=1&showinfo=0"
                    frameborder="2"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                ></iframe>

            </div>
        </>
    )
}

export default EnquiryModal;