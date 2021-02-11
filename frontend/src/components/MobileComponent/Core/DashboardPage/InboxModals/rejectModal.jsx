import React, { useState } from 'react';
// import Swal from 'sweetalert2';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
// import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
// import Loader from '../../../Common/Loader/loader';
// import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
// import { TextArea } from 'formHandler/mobileFormHandler/formFields';
import fileUpload from 'utils/fileUpload';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions/index';
import { showSwal } from 'utils/swal';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const RejectModal = (props) => {
    const { setRejectModal, oi_id, currentPage } = props
    const [filename, setFileName] = useState("Upload Resume");
    const [file, setFile] = useState(undefined);

    const dispatch = useDispatch()
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
            new Promise((resolve, reject) => { dispatch(CandidateAcceptRejectResume({ payload: rejectValues, resolve, reject }));});
            await new Promise((resolve, reject) => dispatch(fetchMyServices({page: currentPage, resolve, reject })));
            dispatch(stopAcceptRejectLoader());

            event.target.reset();
            setFileName("Upload Resume");
            setFile(undefined)
            setRejectModal(false)
            showSwal('success', 'Reject Request Sent!')
        }
        catch {
            dispatch(stopAcceptRejectLoader());
            showSwal('error', 'Something went wrong! Try Again')
        }
    };

    return (
        <>
            { acceptRejectLoader && <Loader /> }
            <div className="m-slide-modal">
                <div className="text-center">
                    <span onClick={() => setRejectModal(false)} className="m-db-close">&#x2715;</span>
                    {/* <h2>Reject Confirmations</h2> */}
                    <p className="fs-16 font-weight-bold mt-20 px-30 mb-15">Get a better resume by sharing us the feedback</p>

                    <p className="error_cls mb-20">
                        { errors.message && "* Either Upload Resume or Leave your comments" }
                    </p>
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="m-db-upload-resume mdb-enquire-now">
                            <div className="m-form-group">
                                <textarea className="m-form-control" id="feedback" placeholder=" " rows="3" name="message" ref={register({
                                    validate: () =>
                                        filename !== "Upload Resume"
                                        ? null
                                        : !getValues("message")
                                            ? errors.message === true
                                            : null,
                                    })} />
                                    <label className="input-label" htmlFor="feedback">Enter Feedback here</label>
                            </div>
                            
                        </div>

                        <div className="mt-20">
                            <p className="mb-0">If you have made any changes resume</p>
                            <div className="m-upload-btn-wrapper">
                                <button className="btn btn-link">{filename}</button>
                                <input type="file" name="file" onChange={(e) => {e.preventDefault(); getFile(e);}} ref={register()}/>
                            </div>
                        </div>
                        <button className="btn btn-primary px-5 mt-10" >Submit</button>
                    </form>
                </div>

            </div>
        </>
    )
}

export default RejectModal;