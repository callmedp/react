import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import './modals.scss'
import Loader from '../../Common/Loader/loader';

const EnquiryModal = (props) => {
    const { setVideoModal, videoUrl, productName } = props
    const { needHelpLoader } = useSelector(store => store.loader);
    const  [faultyVideoUrl, setFaultyVideoUrl] = useState(false);

    const embeddedUrl = (link) => {
        try {
            const url = new URL("https://"+link);
            const id = url.searchParams.get('v');

            if (id == null)
                throw "not valid video url";

            return id;
        } catch {
            setFaultyVideoUrl(true)
        }
    }

    return (
        <>
            {
                needHelpLoader && <Loader />
            }
            <div className="m-container m-enquire-now m-form-pos-btm pb-10" data-aos="fade-up" data-aos-duration="500">
                <span className="m-close" onClick={() => setVideoModal(false)}>x</span>
                <h2 className="m-heading2 text-center">Course Intro</h2>
                <p>{productName}</p>
                {
                    !faultyVideoUrl ? (
                        <iframe width="100%" height="280"
                            src={`https://www.youtube.com/embed/${embeddedUrl(videoUrl)}?autoplay=1&mute=0&controls=1&modestbranding=1&showinfo=0`}
                            frameBorder="2"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                        ></iframe>
                    ) : (
                        <h2>Something went wrong!</h2>
                    )
                }

            </div>
        </>
    )
}

export default EnquiryModal;