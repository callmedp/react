import React from 'react';
import { Modal } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import Loader from '../Loader/loader';

const ReviewModal =(props) => {
    const { videoModal, setVideoModal } = props;
    const { reviewLoader } = useSelector(store => store.loader);
    

    
    //440 315
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
            <iframe width="100%" height="380"
                 src="https://www.youtube.com/embed/65CzisMJpJ0?autoplay=1&mute=0&controls=1&modestbranding=1&showinfo=0" 
                 frameborder="2" 
                 allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                 allowFullScreen
            ></iframe>
            </div>
            </Modal.Body>
        </Modal>
        </>
    )
}

export default ReviewModal;