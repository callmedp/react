import React from 'react';
import './howItWorks.scss';

const HowItWorks = (props) => {
    return (
        <section className="m-container mt-0 mb-0" data-aos="fade-up">
            <div className="m-how-works">
                <h2 className="m-heading2 mb-10">How it will work?</h2>
                <ul>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works1"></i>
                        </figure>
                        <div>
                            <strong className="">Place order</strong>
                            <p>Place order for  the test</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works5"></i>
                        </figure>
                        <div>
                            <strong>Get link</strong>
                            <p>Get test link on mail and sms</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works3"></i>
                        </figure>
                        <div>
                            <strong>Submit test</strong>
                            <p>Complete the test and submit it</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works6"></i>
                        </figure>
                        <div>
                            <strong>Report</strong>
                            <p>Get report of your test</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works7"></i>
                        </figure>
                        <div>
                            <strong>Certificate</strong>
                            <p>Certificate gets added to your shine profile</p>
                        </div>
                    </li>
                </ul>
            </div>
        </section>
    )
}

export default HowItWorks;