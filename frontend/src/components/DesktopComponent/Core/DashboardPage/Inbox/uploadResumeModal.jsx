import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import fileUpload from "utils/fileUpload";
import Swal from 'sweetalert2';
import { useDispatch } from 'react-redux';
import { useForm } from "react-hook-form";
import { uploadResumeForm } from 'store/DashboardPage/MyServices/actions';


const UploadResumeModal =(props) => {
    const { uploadHandelClose, show, data } = props;
    // console.log(data)
    const dispatch = useDispatch();
    let [filename, setFileName] = useState("Upload a file");
    const [file, setFile] = useState(undefined);
    const { register, handleSubmit, errors, getValues, reset } = useForm();

    // for resume upload
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
        console.log(getValues);

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
        <Modal show={show} onHide={uploadHandelClose}>
            <Modal.Header closeButton></Modal.Header>
            <Modal.Body>
                <div className="text-center rate-services db-custom-select-form db-upload-resume">
                    <img src="/media/images/upload-resume.png" className="img-fluid" alt=""/>
                    <p className="rate-services--heading mb-0 mt-0">Upload Resume</p>
                
                    <p className="">To initiate your services, <strong>upload resume</strong></p>
                    {errors.shine_resume && "* Either Upload Resume or use shine resume"}

                    <div className="d-flex align-items-center justify-content-center mt-20">
                        <div className="upload-btn-wrapper">
                            {/* <button className="btn btn-outline-primary">Upload a file</button> */}
                            <form onSubmit={handleSubmit(onSubmit)}>

                                <div className="form-group d-flex align-items-center mt-5">
                                    <div className="upload-btn-wrapper">
                                        <button className="btn btn-outline-primary" >{filename}</button>
                                        <input
                                            type="file"
                                            name="file"
                                            onChange={(e) => {
                                                e.preventDefault();
                                                getFile(e)
                                            }}
                                            ref={register()}
                                        />
                                    </div>
                                </div>
                            </form>
                        </div>

                        <span className="mx-4">Or</span>

                        <div className="custom-control custom-checkbox">
                            <input type="checkbox" className="custom-control-input" id="shineResume" value="True" name="shine_resume" ref={register({
                                validate: () =>
                                filename !== "Upload a file"
                                    ? null
                                    : !getValues("shine_resume")
                                    ? errors.shine_resume === true
                                    : null,
                            })}/> 
                            <label className="custom-control-label font-weight-bold" htmlFor="shineResume">Use shine resume</label>
                        </div>
                    </div>
                    <hr className="my-5"/>

                    {data && data.length > 0 ?
                        <div className="db-upload-resume--services">
                            <strong>Select services</strong> for which you want to use this resume
                            <br/>{errors.resume_course && "* Please Select Atlest One"}

                            <ul className="db-upload-resume--list">
                                {data.map((res,ind) => {
                                    return (
                                        <li className="custom-control custom-checkbox" key={ind}>
                                            <input type="checkbox" className="custom-control-input" name="resume_course" id={res.id} value={res.id} ref={register({validate: () => !getValues("resume_course").length ? errors.resume_course === true : null })}/> 
                                            
                                            <label className="custom-control-label font-weight-bold" htmlFor={res.id}>
                                                {res.product_get_exp_db ? `${res.product_name} ${res.product_get_exp_db}` : res.product_name}
                                            </label>
                                        </li>
                                    )
                                })}
                            </ul>
                        </div>
                        : null 
                    }

                    <button className="btn btn-primary px-5 mt-30" onClick={handleSubmit(onSubmit)}>Save</button>
                </div>
            </Modal.Body>
        </Modal>
    )
}

export default UploadResumeModal;