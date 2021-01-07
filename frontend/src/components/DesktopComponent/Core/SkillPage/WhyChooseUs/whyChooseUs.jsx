import React from 'react';
import './whyChooseUs.scss';

const WhyChooseUs = (props) => {
    return (
        <section className="why-choose-us" id="choose">
        <div className="container">
            <div className="row align-items-center flex-column">
                <h2 className="heading2 mt-10">Why Choose us</h2>
                <ul>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="10">1500<span>+</span></strong>
                        <p data-aos="fade-up" data-aos-delay="30" >jobs available in Digital Marketing</p>
                    </li>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="50">100<span>+</span></strong>
                        <p data-aos="fade-up" data-aos-delay="70">Hiring Partners</p>
                    </li>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="90">10k<span>+</span></strong>
                        <p data-aos="fade-up" data-aos-delay="110">Active learners</p>
                    </li>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="130">24 X 7</strong>
                        <p data-aos="fade-up" data-aos-delay="150">Customer Support</p>
                    </li>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="170">3x</strong>
                        <p data-aos="fade-up" data-aos-delay="190">Increased Chances of Getting Hired</p>
                    </li>
                    <li className="col">
                        <strong data-aos="fade-up" data-aos-delay="210">Self-Paced</strong>
                        <p data-aos="fade-up" data-aos-delay="230">Learning & <strong>Live Classes</strong></p>
                    </li>
                </ul>
            </div>
        </div>
    </section>
    )
}

export default WhyChooseUs;