import React, { useState } from 'react';
import Swal from 'sweetalert2';
import './uploadResume.scss';
import { useDispatch } from 'react-redux';
import { useForm } from "react-hook-form";
import fileUpload from "utils/fileUpload";
import { uploadResumeForm } from 'store/DashboardPage/MyServices/actions';

const UploadResume = (props) => {
    const { setShowUpload, data } = props

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

    const onSubmit = async (values) => {
        values = { ...values, file: file };
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

    return (
        <div className="m-slide-modal">
            <div className="text-center">
                <span onClick={() => setShowUpload(false)} className="m-db-close">X</span>
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
                            data?.map((service) => {
                                return (
                                    <li className="m-custom" key={service?.id}>
                                        <input type="checkbox" id={service?.id} name="resume_course" defaultChecked={true} ref={register({validate: () => !getValues("resume_course").length ? errors.resume_course === true : null })}/>
                                        <label className="font-weight-bold" htmlFor={service?.id}>{service?.product_name}</label>
                                    </li>
                                )
                            })
                        }
                    </ul>
                </div>

                <button className="btn btn-primary px-5 mt-30" onClick={handleSubmit(onSubmit)}>Save</button>
            </div>

        </div>
    )
}

export default UploadResume;