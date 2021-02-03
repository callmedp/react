import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import './uploadResume.scss';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from "react-hook-form";
import fileUpload from "utils/fileUpload";
import { uploadResumeForm } from 'store/DashboardPage/MyServices/actions';
import { fetchPendingResume } from 'store/DashboardPage/MyServices/actions/index';
import { startUploadLoader, stopUploadLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const UploadResume = (props) => {
    const { setShowUpload } = props

    let [filename, setFileName] = useState("Upload a file");
    const [file, setFile] = useState(undefined);
    const dispatch = useDispatch()
    const { register, handleSubmit, errors, getValues, reset } = useForm();

    const getFile = (event) => {
        let fileName = event.target.files[0].name
        let fileUploadValue = fileUpload(event)

        if(fileUploadValue){
            setFileName(fileName);
            setFile(fileUploadValue)
        }
    }

    const handleEffects = async () => {
        try{
            dispatch(startUploadLoader());
            await new Promise((resolve, reject) => dispatch(fetchPendingResume({payload : {}, resolve, reject})));
            dispatch(stopUploadLoader());
        }
        catch(e){
            dispatch(stopUploadLoader());
        }
    };

    const pending_resume_items = useSelector(store => store.dashboardPendingResume.data);
    const { uploadLoader } = useSelector(store => store.loader);

    const onSubmit = async (values) => {
        values = { ...values, file: file };
        console.log(values)
        let response = await new Promise((resolve, reject) => {
            dispatch(uploadResumeForm({ values, resolve, reject }));
        });

        if (!response.error) {
            reset();
            Swal.fire({
                icon: "success",
                title: "Form Submitted Successfully"
            })
            setFile(undefined)
            setFileName("Upload a file");
        }
        else {
            Swal.fire({
                icon: "error",
                title: "Oops! <br> Something went wrong! Try Again"
            })
        }
    }

    useEffect(() => {
        handleEffects()
    }, [])

    return (
        <>
        {
            uploadLoader && <Loader />
        }
        <div className="m-slide-modal">
            <div className="text-center">
                <span onClick={() => setShowUpload(false)} className="m-db-close">&#x2715;</span>
                <h2>Upload Resume </h2>
                <p>To initiate your services, <strong>upload resume</strong></p>

                <span className="error_cls">
                    {errors.shine_resume && "* Either Upload Resume or use shine resume"}
                </span>
                
                <div className="d-flex align-items-center justify-content-center mt-20">
                    <div className="m-upload-btn-wrapper">
                        <button className="btn btn-blue-outline">{filename}</button>
                        <input type="file" name="file" onChange={(e) => { e.preventDefault(); getFile(e) }} ref={register()}/>
                    </div>

                    <span className="mx-4">Or</span>

                    <div className="m-custom">
                        <input type="checkbox" id="shine_resume" name='shine_resume' ref={register({
                                validate: () =>
                                filename !== "Upload a file"
                                    ? null
                                    : !getValues("shine_resume")
                                    ? errors.shine_resume === true
                                    : null,
                            })}
                        />
                        <label className="m-custom--label font-weight-bold mb-0" htmlFor="shine_resume">Use shine resume</label>
                    </div>
                </div>

                <hr className="my-20" />

                <div className="m-db-upload-resume">
                    <strong>Select services</strong> for which you want to use this resume
                    <br />
                    <span className="error_cls">
                        {errors.resume_course && "* Please Select Atlest One Service"}
                    </span>
                    <ul className="m-db-upload-resume--list">
                        {
                            pending_resume_items?.map((service) => {
                                return (
                                    <li className="m-custom" key={service?.id}>
                                        <input type="checkbox" id={service?.id} name="resume_course" defaultChecked={true} value={service?.id} ref={register({validate: () => !getValues("resume_course").length ? errors.resume_course === true : null })}/>
                                        <label className="font-weight-bold" htmlFor={service?.id}>{service?.product_name}</label>
                                    </li>
                                )
                            })
                        }
                    </ul>
                </div>

                <button className="btn btn-primary px-5 mt-30" onClick={handleSubmit(onSubmit)}>Upload</button>
            </div>

        </div>
        </>
    )
}

export default UploadResume;