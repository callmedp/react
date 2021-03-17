// React Core Import
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

// Form Import
import { useForm } from 'react-hook-form';

// Styling Import
import './enquireNow.scss';

const EnquireNow = (props) => {
    const { history } = props;
    const { register, handleSubmit, errors } = useForm();

    const addValues = (values) => {
        // Adding and contributing their values according to contributions
    }
    
    return (
        <section id="enquire-now" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="enquire-now mt-30 mb-30">
                        <div className="enquire-now__img col">
                            <img src="/media/images/desktop/enquire-now-bg.png" alt="Enquire Now" />
                        </div>
                        <div className="enquire-now__form col">
                            <strong className="heading2">Enquire now!</strong>
                            <form className="mt-30">
                                <div className="form-group error">
                                    <input type="text" className="form-control" id="name" name="name" placeholder=" "
                                        value="" aria-required="true" aria-invalid="true" />
                                    <label for="">Name</label>
                                    <span class="error-msg">Required</span>
                                </div>
                                <div className="d-flex">
                                    <div className="custom-select-box">
                                        <select className="select" className="custom-select">
                                            <option selected>+91</option>
                                            <option value="+91">+91</option>
                                            <option value="+92">+92</option>
                                            <option value="+93">+93</option>
                                        </select>
                                    </div>
                                    <div className="form-group flex-1">
                                        <input type="text" className="form-control" id="mobile" name="mobile"
                                            placeholder=" " value="" aria-required="true" aria-invalid="true" />
                                        <label for="">Mobile</label>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <textarea className="form-control" rows="3" id="mesage" name="mesage" placeholder=" "
                                        value="" aria-required="true" aria-invalid="true" />
                                    <label for="">Message</label>
                                </div>
                                <button type="submit" className="btn btn-inline btn-primary submit-btn" role="button">Submit</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default EnquireNow;