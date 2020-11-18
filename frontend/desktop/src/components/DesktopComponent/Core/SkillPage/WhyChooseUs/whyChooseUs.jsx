import React from 'react';
import './whyChooseUs.scss';

const WhyChooseUs = (props) => {
    return (
        <section className="why-choose-us">
        <div className="container">
            <div className="row align-items-center flex-column">
                <h2 className="heading2">Why Choose us</h2>
                <ul>
                    <li className="col">
                        <figure className="icon-choose1"></figure>
                        <strong>36000+ Jobs</strong>
                        <p>opportunities on shine</p>
                    </li>
                    <li className="col">
                        <figure className="icon-choose2"></figure>
                        <strong>Application Highlighter</strong>
                        <p>worth Rs 1600 Free for 90 Days</p>
                    </li>
                    <li className="col">
                        <figure className="icon-choose3"></figure>
                        <strong>Interview Prep Assistance</strong>
                        <p>Exclusive Interview Preparation Handbook & Free Mock Interview with Expert*</p>
                    </li>
                    <li className="col">
                        <figure className="icon-choose4"></figure>
                        <strong>Industry Recognized Certification</strong>
                        <p>Certificate by Analytics Vidhya with lifetime validity.</p>
                    </li>
                    <li className="col">
                        <figure className="icon-choose5"></figure>
                        <strong>Customer Support</strong>
                        <p>over calls and emails</p>
                    </li>
                    <li className="col">
                        <figure className="icon-choose6"></figure>
                        <strong>Chat With Mentors</strong>
                        <p>1 Hour Chat with mentors Daily</p>
                    </li>
                </ul>
            </div>
        </div>
    </section>
    )
}

export default WhyChooseUs;