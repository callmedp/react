import React from 'react';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';
import './modals.scss'

const EnquiryModal = (props) => {
    return(
        <div class="m-container m-enquire-now m-form-pos-btm pb-10">
            <span className="m-close">x</span>
            <h2 className="m-heading2 text-center">Enquire now!</h2>
            <p className="text-center">Share your query, our experts will help you take  your career forward!</p>
            <form className="mt-20">
                <div className="m-form-group">
                    <input className="m-input_field" type="text" name="name" id="name" placeholder=" " />
                    <label className="m-input_label" for="name">Name*</label>
                </div>
                <div className="m-form-group m-error">
                    <input type="text" className="input_field" name="email" id="email" placeholder=" " />
                    <label className="m-input_label" for="email">Email*</label>
                </div>
                <div className="d-flex">
                    <div className="m-custom-select-box">
                        <select name="country_code" className="m-custom-select">
                            <option value="91">+91</option>
                            <option value="92">+92</option>
                        </select>
                    </div>
                    <div className="m-form-group flex-1">
                        <input className="input_field" type="number" name="cell_phone" id="cell_phone" placeholder=" " value="" />
                        <label className="m-input_label" for="cell_phone">Mobile*</label>
                    </div>
                </div>
                <div className="m-form-group">
                    <button className="btn-blue">Submit</button>
                </div>

            </form>
        </div>
    )
}

export default EnquiryModal;