import React from 'react';
import './whyChooseUs.scss';

const WhyChooseUs = (props) => {
    return (
        <section className="why-choose-us" id="choose">
        <div className="container">
            <div className="row align-items-center flex-column">
                <h2 className="heading2 mt-10">Why Choose us</h2>
                <ul>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="10" class="icon-choose1"></figure>
                        <strong data-aos="fade-up" data-aos-delay="30">36000+ Jobs</strong>
                        <p data-aos="fade-up" data-aos-delay="50" >opportunities on shine</p>
                    </li>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="70" class="icon-choose2"></figure>
                        <strong data-aos="fade-up" data-aos-delay="90">Application Highlighter</strong>
                        <p data-aos="fade-up" data-aos-delay="110">worth Rs 1600 Free for 90 Days</p>
                    </li>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="130" class="icon-choose3"></figure>
                        <strong data-aos="fade-up" data-aos-delay="150">Interview Prep Assistance</strong>
                        <p data-aos="fade-up" data-aos-delay="170">Exclusive Interview Preparation Handbook & Free Mock Interview with Expert*</p>
                    </li>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="190" class="icon-choose4"></figure>
                        <strong data-aos="fade-up" data-aos-delay="210">Industry Recognized Certification</strong>
                        <p data-aos="fade-up" data-aos-delay="230">Certificate by Analytics Vidhya with lifetime validity.</p>
                    </li>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="250" class="icon-choose5"></figure>
                        <strong data-aos="fade-up" data-aos-delay="270">Customer Support</strong>
                        <p data-aos="fade-up" data-aos-delay="290">over calls and emails</p>
                    </li>
                    <li class="col">
                        <figure data-aos="fade-up" data-aos-delay="310" class="icon-choose6"></figure>
                        <strong data-aos="fade-up" data-aos-delay="330">Chat With Mentors</strong>
                        <p data-aos="fade-up" data-aos-delay="350">1 Hour Chat with mentors Daily</p>
                    </li>
                </ul>
            </div>
        </div>
    </section>
    )
}

export default WhyChooseUs;