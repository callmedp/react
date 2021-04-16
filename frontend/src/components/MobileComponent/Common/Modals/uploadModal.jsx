import React from 'react';
import {Link} from 'react-router-dom';
import Modal from 'react-modal';
import './modals.scss'
 
const UploadModal = (props) => {
    return(
        <div className="m-container m-enquire-now m-upload-modal m-form-pos-btm pb-10">
            <span className="m-close">x</span>
            <h2 className="m-heading2 text-center">Upload Resume</h2>
            <p className="text-center">Increases the chances of getting more opportunities, with latest resume</p>
            <form className="mt-20">
                <div className="upload-btn-wrapper">
                    <button className="btn-upload">Choose file<input type="file" name="myfile" /></button>
                </div>
                <span className="small mt-20">File size should not exceed 3MB. in .doc, PDF, Jpeg format only</span>
                <div className="m-form-group text-center mt-20">
                    <button className="btn-blue">Save</button>
                </div>
                
            </form>
        </div>
    )
}

export default UploadModal;