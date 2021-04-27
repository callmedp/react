import React from 'react';
import { Link } from 'react-router-dom';
import './howItWorks.scss';

const HowItWorks1 = (props) => {

    return (
        <section id="howitworks" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-40">
                    <div className="how-works">
                        <h2 className="heading2 text-center">How it will work?</h2>
                        <ul className="mt-30">
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works1"></i>
                                </figure>
                                <strong className="">Place order</strong>
                                <p>Place order for the test</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works5"></i>
                                </figure>
                                <strong>Get link</strong>
                                <p>Get test link on mail and sms</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works3"></i>
                                </figure>
                                <strong>Submit test</strong>
                                <p>Complete the test and submit it</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works6"></i>
                                </figure>
                                <strong>Report</strong>
                                <p>Get report of your test</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works7"></i>
                                </figure>
                                <strong>Certificate</strong>
                                <p>Certificate gets added to your shine profile</p>
                            </li>
                        </ul>
                        <div className="d-flex justify-content-center mt-50">
                            <Link to={"#"} className="btn btn-outline-primary btn-custom">Enquire now</Link>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default HowItWorks1;