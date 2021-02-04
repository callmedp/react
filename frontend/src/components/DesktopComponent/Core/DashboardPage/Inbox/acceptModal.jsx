import React from 'react';
import {Toast} from '../../../Common/Toast/toast';
import { Modal } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';

const AcceptModal = (props) => {
    const { acceptModal, setAcceptModal, oi_id } = props
    const dispatch = useDispatch()

    const acceptRejectHandler = async (type, id) => {
        if (type === "accept") {
            let acceptValues = {
                oi_pk: id,
                type
            }
        try {
                dispatch(startAcceptRejectLoader());
                await new Promise((resolve, reject) => { dispatch(CandidateAcceptRejectResume({ payload: acceptValues, resolve, reject })); });
                dispatch(stopAcceptRejectLoader());

                Toast.fire({
                    type: 'success',
                    title: 'Accept Request Sent!'
                });

                setAcceptModal(false);
            }
            catch (e) {
                dispatch(stopAcceptRejectLoader());

                Toast.fire({
                    type: 'error',
                    title: 'Something went wrong! Try Again'
                });
            }
        }
    };

    return (
        <Modal show={acceptModal} onHide={setAcceptModal}>
            <Modal.Header closeButton></Modal.Header>
            <Modal.Body></Modal.Body>
            <div className="text-center pl-30 pr-30 pb-30">
                <h2>Accept Confirmation </h2>
                <strong>Are you sure you want to accept?</strong>
                <br />
                <span>Note: Once you accept, your service will be closed.</span>
                <br /> <br/>
                <button className="btn btn-blue" onClick={() => acceptRejectHandler("accept", oi_id)}>Accept</button>&emsp;
                <button className="btn btn-blue-outline" onClick={() => setAcceptModal(false)}>Skip</button>
            </div>
        </Modal>
    )
}

export default AcceptModal;