import React, { useState } from 'react';
import Swal from 'sweetalert2';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import { CandidateAcceptRejectResume } from 'store/DashboardPage/MyServices/actions/index';
import { startAcceptRejectLoader, stopAcceptRejectLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { TextArea } from 'formHandler/mobileFormHandler/formFields';
import fileUpload from 'utils/fileUpload';

const RejectModal = (props) => {
    const { setRejectModal, oi_id } = props
    const [filename, setFileName] = useState("Upload Your Resume");
    const [file, setFile] = useState(undefined);

    const dispatch = useDispatch()
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
            await new Promise((resolve, reject) => { dispatch(CandidateAcceptRejectResume({ payload: rejectValues, resolve, reject }));});
            event.target.reset();
            setFileName("Upload Your Resume");
            setFile(undefined)
            setRejectModal(false)
        }
        catch {
            Swal.fire({
                icon: "error",
                title: "Something went wrong! Try Again",
            });
        }
    };

    return (
        <div className="m-slide-modal">
            <div className="text-center">
                <span onClick={() => setRejectModal(false)} className="m-db-close">&#x2715;</span>
                <h2>Reject Confirmationsddsd </h2>
                <br/>
                <p>If you have made changes to document, please upload here</p>

                <span className="error_cls">
                    { errors.message && "* Either Upload Resume or Leave your comments" }
                </span>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="d-flex align-items-center justify-content-center mt-20">
                        <div className="m-upload-btn-wrapper">
                            <button className="btn btn-blue-outline">{filename}</button>
                            <input type="file" name="file" onChange={(e) => {e.preventDefault(); getFile(e);}} ref={register()}/>
                        </div>

                    </div>

                    <hr className="my-20" />
                    <span className="mx-4"><strong>Or</strong></span>

                    <div className="m-db-upload-resume">
                        <br /> 
                        
                        <div className="m-form-group">
                            <textarea className="form-control" placeholder="Leave us your message" rows="3" name="message" ref={register({
                                validate: () =>
                                    filename !== "Upload Your Resume"
                                    ? null
                                    : !getValues("message")
                                        ? errors.message === true
                                        : null,
                                })} />
                        </div>
                        
                    </div>

                    <button className="btn btn-primary px-5 mt-30" >Submit</button>
                </form>
            </div>

        </div>
    )
}

export default RejectModal;