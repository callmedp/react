import React from 'react';
import {Toast} from '../../../Common/Toast/toast';
import Swal from 'sweetalert2';
import { Modal } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions';
import Loader from '../../../Common/Loader/loader';

const AcceptModal = (props) => {
    const { acceptModal, setAcceptModal, oi_id, filterState, currentPage } = props
    const { acceptRejectLoader } = useSelector(store => store.loader);
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
                await new Promise((resolve, reject) => dispatch(fetchMyServices({ page: currentPage, isDesk: true, ...filterState, resolve, reject })))
                dispatch(stopAcceptRejectLoader());

                Swal.fire({
                    icon: 'success',
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
        <>
            { acceptRejectLoader && <Loader /> }
            <Modal show={acceptModal} onHide={setAcceptModal} className="db-page">
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body></Modal.Body>
                <div className="text-center pl-30 pr-30 pb-30 mb-30">
                    <p className="font-weight-bold mb-0 fs-16">Are you sure you want to accept?</p>
                    <p className="mb-4">Once you accept it , this service will be closed</p>
                    <button className="btn btn-outline-primary px-5" onClick={() => acceptRejectHandler("accept", oi_id)}>Accept</button>
                </div>
            </Modal>
        </>
    )
}

export default AcceptModal;