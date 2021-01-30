import React from 'react';
import { Link } from 'react-router-dom';
import './practiceTestBanner.scss'

const PracticeTestBanner = (props) => {
    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="m-practice-test m-lightblue-bg">
                <figure>
                    <img src="./media/images/mobile/practice-test-bg.png" className="img-fluid w-100" alt="Practice Test" />
                </figure>
                <strong>Take our free practice test to help you choose the right course.</strong>
                <Link className="btn-blue-outline mb-20" to={"#"}>Take free test</Link>
            </div>
        </section>
    )
}

export default PracticeTestBanner;