import React, { useState } from 'react';
import Swal from 'sweetalert2';
import { Modal } from 'react-bootstrap';
import {Toast} from '../../../Common/Toast/toast';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import fileUpload from 'utils/fileUpload';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions';
import Loader from '../../../Common/Loader/loader';

const RejectModal = (props) => {
    const { rejectModal, setRejectModal, oi_id, currentPage, filterState } = props
    const [filename, setFileName] = useState("Upload here");
    const [file, setFile] = useState(undefined);
    const dispatch = useDispatch();
    const { acceptRejectLoader } = useSelector(store => store.loader);
    const { register, handleSubmit, errors, reset, getValues } = useForm();

    const getFile = (event) => {
        let fileName = event.target.files[0].name
        let fileUploadValue = fileUpload(event)

        if(fileUploadValue){
            setFileName(fileName);
            setFile(fileUploadValue)
        }
    }

    const onSubmit = async (values, event) => {
        let rejectValues = {
            ...values,
            file: file,
            oi: oi_id,
            type: "reject",
        }

        try {
            dispatch(startAcceptRejectLoader());
            await new Promise((resolve, reject) => { dispatch(CandidateAcceptRejectResume({ payload: rejectValues, resolve, reject }));});
            await new Promise((resolve, reject) => dispatch(fetchMyServices({ page: currentPage, isDesk: true, ...filterState, resolve, reject })))
            dispatch(stopAcceptRejectLoader());

            event.target.reset();
            setFileName("Upload here");
            setFile(undefined);
            setRejectModal(false);
            Swal.fire({
                icon: 'success',
                title: 'Reject Request Sent!'
            });
        }
        catch {
            dispatch(stopAcceptRejectLoader());

            Toast.fire({
                type: 'error',
                title: 'Something went wrong! Try Again'
            });
        }
    };

    return (
        <>
            { acceptRejectLoader && <Loader /> }
            <Modal show={rejectModal} onHide={setRejectModal} className="db-page modal-dialog-centered">
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body>
                    <div className="text-center">
                        <p className="fs-16 font-weight-bold px-5">Get a better resume by sharing us the feedback</p>

                        <div className="form-group">
                            <textarea className="form-control" placeholder="Leave us your message" rows="3" name="message" ref={register({
                                validate: () =>
                                    filename !== "Upload here"
                                        ? null
                                        : !getValues("message")
                                            ? errors.message === true
                                            : null,
                            })} />
                        </div>

                        <span className="error_cls">
                            { errors.message && "* Either Upload Resume or Leave your comments" }
                        </span>
                        <form onSubmit={handleSubmit(onSubmit)}>
                            <div className="d-flex align-items-center justify-content-center mt-20">
                                <p className="fs-12">If you have made changes in resume</p>
                                <div className="upload-btn-wrapper">
                                    <span className="db-reject-upload-here">{filename}</span>
                                    <input type="file" name="file" onChange={(e) => {e.preventDefault(); getFile(e);}} ref={register()}/>
                                </div>
                            </div>
                            <button className="btn btn-primary px-5 mt-30" >Submit</button>
                        </form>
                    </div>
                </Modal.Body>
            </Modal>
        </>
    )
}

export default RejectModal;