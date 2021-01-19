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
                        <p>
                            <strong>1500<span>+</span></strong>
                            jobs available in Digital Marketing
                        </p>
                    </li>
                    <li>
                        <p>
                            <strong>100<span>+</span></strong>
                            Hiring Partners
                        </p>
                    </li>
                    <li>
                        <p>
                            <strong>10k<span>+</span></strong>
                            Active learners
                        </p>
                    </li>
                    <li>
                        <p>
                            <strong>24 X 7</strong>
                            Customer Support
                        </p>
                    </li>
                    <li>
                        <p>
                            <strong>3x</strong>
                            Increased Chances of Getting Hired
                        </p>
                    </li>
                    <li>
                        <p>
                            <strong>Self-Paced</strong>
                            Learning & <span>Live Classes</span>
                        </p>
                    </li>
                </ul>
            </div>
        </div>
        </section>
    )
}

export default WhyChooseUs;