import React, { useState } from 'react';
import { Modal } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import Loader from '../Loader/loader';

const ReviewModal = (props) => {
    const { videoModal, setVideoModal, videoUrl, productName } = props;
    const { reviewLoader } = useSelector(store => store.loader);
    const [faultyVideoUrl, setFaultyVideoUrl] = useState(false);

    const embeddedUrl = (link) => {
        try {
            const url = new URL("https://"+link);
            const id = url.searchParams.get('v');

            if(id == null)
                throw "not valid video url";

            return id;
        } catch {
            setFaultyVideoUrl(true)
        }
    }

    return (
        <>
            { reviewLoader ? <Loader /> : ''}
            <Modal show={videoModal}
                onHide={() => setVideoModal(false)}
                className="db-modal db-page"
                dialogClassName="modal-lg"
            >
                <Modal.Header closeButton></Modal.Header>

                <Modal.Body>
                    <div className="">
                        <h2>Course Intro</h2>
                        <p>{productName}</p>
                        {
                            !faultyVideoUrl ? (
                                <iframe width="100%" height="380"
                                    src={`https://www.youtube.com/embed/${embeddedUrl(videoUrl)}?autoplay=1&mute=0&controls=1&modestbranding=1&showinfo=0`}
                                    frameBorder="2"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowFullScreen
                                ></iframe>
                            ) : (
                                <strong>Something went wrong!</strong>
                            )
                        }
                    </div>
                </Modal.Body>
            </Modal>
        </>
    )
}

export default ReviewModal;