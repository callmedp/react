import React from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';


const FindJobEdit = (props) => {
    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
                    <div className="m-ui-main col">
                        <div className="d-flex align-items-center">
                            <div className="m-ui-steps">
                                <Link className="m-completed" to={"#"}>1</Link>
                                <Link className="m-current" to={"#"}>2</Link>
                                <Link>3</Link>
                            </div>
                            <Link className="btn-blue-outline m-back-goal-btn">Back to goal</Link>
                        </div>

                        <h2 className="m-heading3 mt-20">Let’s get you to the right job</h2>
                                <div className="m-find-job">
                                    <form className="mt-20">
                                        <div className="form-group">
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" "
                                                value="Sr. Sales Manager" aria-required="true" aria-invalid="true" />
                                            <label for="">Current job title</label>
                                        </div>
                                        <div className="form-group">
                                            <div className="custom-select-box">
                                                <select className="select" className="custom-select">
                                                    <option selected>Total experience </option>
                                                    <option value="+91">1 - 2</option>
                                                    <option value="+92">3 - 5</option>
                                                    <option value="+93">6+</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div className="form-group">
                                            <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                                value="Delhi NCR" aria-required="true" aria-invalid="true" />
                                            <label for="">Preferred location</label>
                                        </div>
                                        <div className="form-group-custom pos-rel">
                                            <label className="sticky-label" for="">Your skills</label>
                                            <div className="custom-textarea">
                                                <label className="label-added" for="">Advanced Accounting</label>
                                                <label className="label-added" for="">Risk Management</label>
                                                <label className="label-added" for="">GST</label>
                                                <label className="label-added" for="">Data Science</label>
                                                <label className="label-added" for="">Six Sigms</label>
                                                <span className="d-flex align-items-center mt-10">
                                                    <input type="text" className="form-control custom-input" placeholder="Keyword Research" />
                                                </span>
                                            </div>
                                        </div>
                                        <div className="form-group-custom">
                                            <label className="label-add" for="">Advanced Accounting</label>
                                            <label className="label-add" for="">Risk Management</label>
                                            <label className="label-add" for="">GST</label>
                                            <label className="label-add" for="">Data Science</label>
                                            <label className="label-add" for="">Six Sigms</label>
                                        </div>
                                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                        data-target="#thankyouModal">View jobs</button>
                                    </form>
                                </div>
                            </div>
        </section>
    )
}

export default FindJobEdit;