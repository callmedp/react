import React from 'react';
import './keyFeatures.scss';

const WhatYouGet = (props) => {
    const {prd_vendor_slug} = props;

    return (
        <section id="keyfeatures" className="container-fluid mb-0">
            <div className="row">
                <div className="container">
                    <div className="key-features mb-20">
                        {prd_vendor_slug === 'testpreptraining' ?
                            <>
                                <h2 className="heading2">What you get?</h2>
                                <ul className="mt-20">
                                    <li>Industry recognized certification after clearing the test</li>
                                    <li>Get badge on shine.com and showcase your knowledge to the recruiters</li>
                                    <li>Shine shows your skills as validated and certification as verified which build high trust among recruiters</li>
                                    <li>Receive valuable feedback on your strong and weak areas to improve yourself</li>
                                    <li>Certified candidate gets 1 month complimentary featured profile</li>
                                    <li>Get Q & A Support (for all learners at shine learning)</li>
                                </ul>
                            </>
                            :
                            <>
                                <h2 className="heading2">What you get if you pass?</h2>
                                <ul className="mt-20">
                                    <li>Receive valuable feedback, from reliable exam reports, on your strong and weak areas</li>
                                    <li>Get real exam and practice environment</li>
                                    <li>In depth and exhaustive explanation to every question to enhance your learning</li>
                                    <li>Unlimited access to the assessment platform</li>
                                    <li>500+ questions to test your learning on variety of topics</li>
                                    <li>Gets Tips & Tricks to crack the test</li>
                                </ul>
                            </>
                        }
                    </div>
                </div>
            </div>
        </section>
    )
}


export default WhatYouGet;