import React from 'react';
import { Link } from 'react-router-dom';
import './leadCampaignPage.scss';
import CampaignHeader from '../../Common/CampaignHeader/campaignHeader';
import CampaignFooter from '../../Common/CampaignFooter/campaignFooter';

const LeadCampaignPage = (props) => {
    return (
        <div>
            <CampaignHeader />
            <section className="container-fluid">
                <div className="row">
                    <div className="ja-langingpage mx-auto">
                        <div className="ja-form">
                            <div className="ja-form__img">
                                <h1 className="heading1 ml-30 mt-70">100% guaranteed Job Assistance Programs</h1>
                                <ul>
                                    <li>Google/Azure Certification </li>
                                    <li>Datascience </li>
                                    <li>Six Sigma</li>
                                    <li>Project Management</li>
                                    <li>Digital Marketing</li>
                                    <li>Amazon Web Services ( AWS Certification)</li>
                                </ul>
                            </div>
                            <div className="ja-form__form flex-1">
                                <form className="mt-30">
                                    <div className="form-group error">
                                        <input type="text" className="form-control" id="name" name="name" placeholder=" "
                                            value="" aria-required="true" aria-invalid="true" />
                                        <label for="">Name</label>
                                        <span className="error-msg">Required</span>
                                    </div>
                                    <div className="form-group">
                                        <input type="text" className="form-control" id="email" name="email" placeholder=" "
                                            value="" aria-required="true" aria-invalid="true" />
                                        <label for="">Email</label>
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
                                        <div className="custom-select-box w-100">
                                            <select className="select" className="custom-select">
                                                <option selected>Interested Certification </option>
                                                <option value="">Certification 1</option>
                                                <option value="">Certification 2</option>
                                                <option value="">Certification 3</option>
                                            </select>
                                        </div>
                                    </div>
                                    <button type="submit" className="btn btn-primary submit-btn w-100" role="button">Submit</button>
                                </form>
                                <div className="social-links-lp mx-auto mt-50">
                                    <p>Follow us on :</p>
                                    <Link to="#" className="icon-fb-ja"></Link>
                                    <Link to="#" className="icon-linkedin-ja"></Link>
                                    <Link to="#" className="icon-twitter-ja"></Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <CampaignFooter />
        </div>
    )
};

export default LeadCampaignPage;