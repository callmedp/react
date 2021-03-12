import React from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';
import { imageUrl } from 'utils/domains';


const FindJobEdit = (props) => {
    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="current" to={"#"}>2</Link>
                            <Link>3</Link>
                        </div>

                        <h2 className="heading3 mt-20">Let’s get you to the right job</h2>
                        <div className="d-flex">
                            <div className="w-50">
                                <div className="find-job">
                                    <form className="mt-20">
                                        <div className="form-group checked">
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" "
                                                value="Sr. Sales Manager" aria-required="true" aria-invalid="true" />
                                            <label for="">Current job title</label>
                                        </div>
                                        <div className="form-group checked">
                                            <div className="custom-select-box">
                                                <select className="select" className="custom-select">
                                                    <option selected>Total experience </option>
                                                    <option value="+91">1 - 2</option>
                                                    <option value="+92">3 - 5</option>
                                                    <option value="+93">6+</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div className="form-group checked">
                                            <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                                value="Delhi NCR" aria-required="true" aria-invalid="true" />
                                            <label for="">Preferred location</label>
                                        </div>
                                        <div className="form-group-custom checked">
                                            <label className="sticky-label" for="">Your skills</label>
                                            <div className="custom-textarea">
                                                <label className="label-added" for="">Advanced Accounting</label>
                                                <label className="label-added" for="">Risk Management</label>
                                                <label className="label-added" for="">GST</label>
                                                <label className="label-added" for="">Data Science</label>
                                                <label className="label-added" for="">Six Sigms</label>
                                                <span className="d-flex align-items-center mt-10">
                                                    <input type="text" className="form-control custom-input" placeholder="Keyword Research" />
                                                    <button className="custom-btn" type="submit"><figure className="icon-search-arrow"></figure></button>
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
                            <figure className="find-job-bg">
                                <img src={`${imageUrl}desktop/find-right-job.png`} className="img-fluid" alt="Let’s get you to the right job" />
                            </figure>
                        </div>
                        
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FindJobEdit;