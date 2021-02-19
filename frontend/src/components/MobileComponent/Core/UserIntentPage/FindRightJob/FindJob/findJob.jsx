import React from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';


const FindJob = (props) => {
    const { history, type } = props;
    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-current" to={"#"}>2</Link>
                        <Link>3</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <h2 className="m-heading3 mt-20">{ type === 'job' ? 'Let’s get you to the right job' : type === 'pcareer' ? 'Get to next level with shine' : 'What do you have in mind' }</h2>

                        <div className="m-find-job">
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
                                    </div>
                                </div>
                                <div className="form-group">
                                    <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                        aria-required="true" aria-invalid="true" />
                                    <label for="">Preferred location</label>
                                </div>
                                <div className="form-group">
                                    <input type="text" className="form-control" id="skills" name="skills" placeholder=" "
                                        aria-required="true" aria-invalid="true" />
                                    <label for="">Your skills</label>
                                </div>
                                <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                data-target="#thankyouModal">{ type === 'job' ? 'View jobs' : 'View courses' }</button>
                            </form>
                        </div>
                    </div>
        </section>
    )
}

export default FindJob;