import React from 'react';
import './needHelp.scss';

const NeedHelp = (props) => {
    return (
            <div className="need-help">
                <strong className="heading2">Need Help?</strong>
                <form className="mt-20">
                    <div className="d-flex">
                        <div className="custom-select-box">
                            <select className="select" className="custom-select">
                                <option selected>+91</option>
                                <option value="+91">+91</option>
                                <option value="+92">+92</option>
                                <option value="+93">+93</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <input type="text" className="form-control" id="mobile" name="mobile"
                                placeholder=" " value="" aria-required="true" aria-invalid="true" />
                            <label for="">Mobile</label>
                        </div>
                    </div>
                    <div className="form-group error">
                        <input type="email" className="form-control" id="email" name="email" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Email</label>
                        <span class="error-msg">Required</span>
                    </div>
                    <div className="form-group">
                        <input type="text" className="form-control" id="name" name="name" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Name</label>
                    </div>
                    <button type="submit" className="btn btn-inline btn-primary mx-auto submit-btn" role="button" data-toggle="modal"
                    data-target="#thankyouModal">Submit</button>
                </form>
            </div>
    )
}

export default NeedHelp;