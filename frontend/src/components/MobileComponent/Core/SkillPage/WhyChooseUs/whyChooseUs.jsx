import React from 'react';
import './whyChooseUs.scss';

const WhyChooseUs = (props) => {
    return (
        <section className="m-why-choose-us mt-0 mb-0" data-aos="fade-up">
        <div className="m-container pt-10">
            <div className="align-items-center flex-column">
                <h2 className="m-heading2">Why Choose us</h2>
                <ul>
                    <li>
                        <figure className="micon-choose1"></figure>
                        <p>
                            <strong>36000+ Jobs</strong>
                            opportunities on shine
                        </p>
                    </li>
                    <li>
                        <figure className="micon-choose2"></figure>
                        <p>
                            <strong>Application Highlighter</strong>
                            worth Rs 1600 Free for 90 Days
                        </p>
                    </li>
                    <li>
                        <figure className="micon-choose3"></figure>
                        <p>
                            <strong>Interview Prep Assistance</strong>
                            Exclusive Interview Preparation Handbook & Free Mock Interview with Expert*
                        </p>
                    </li>
                    <li>
                        <figure className="micon-choose4"></figure>
                        <p>
                            <strong>Industry Recognized Certification</strong>
                            Certificate by Analytics Vidhya with lifetime validity.
                        </p>
                    </li>
                    <li>
                        <figure className="micon-choose5"></figure>
                        <p>
                            <strong>Customer Support</strong>
                            over calls and emails
                        </p>
                    </li>
                    <li>
                        <figure className="micon-choose6"></figure>
                        <p>
                            <strong>Chat With Mentors</strong>
                            1 Hour Chat with mentors Daily
                        </p>
                    </li>
                </ul>
            </div>
        </div>
        </section>
    )
}

export default WhyChooseUs;