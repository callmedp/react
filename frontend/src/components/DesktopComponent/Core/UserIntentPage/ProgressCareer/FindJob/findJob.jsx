import React from 'react';
import { Link } from 'react-router-dom';
import '../../FindRightJob/FindJob/findJob.scss';


const FindJob = (props) => {
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

                        <h2 className="heading3 mt-20">Get to the next level with shine</h2>
                        <div className="d-flex">
                            <div className="w-50">
                                <div className="find-job">
                                    <form className="mt-20">
                                        <div className="form-group">
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
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
                                                <label for="">Total experience</label>
                                            </div>
                                        </div>
                                        <div className="form-group error">
                                            <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Preferred location</label>
                                            <span class="error-msg">Required</span>
                                        </div>
                                        <div className="form-group">
                                            <input type="text" className="form-control" id="skills" name="skills" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Your skills</label>
                                        </div>
                                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                        data-target="#thankyouModal">View courses</button>
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

export default FindJob;