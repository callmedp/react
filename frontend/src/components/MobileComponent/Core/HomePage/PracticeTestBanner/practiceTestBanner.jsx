import React from 'react';
import { Link } from 'react-router-dom';
import { siteDomain, imageUrl } from 'utils/domains';
import './practiceTestBanner.scss'

const PracticeTestBanner = (props) => {

    // const testRedirect = (slug) => {
    //     window.location.replace(`${siteDomain}/practice-tests/`);
    // } 

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="m-practice-test m-lightblue-bg">
                <figure>
                    <img src={`${imageUrl}/mobile/practice-test-bg.png`} className="img-fluid w-100" alt="Practice Test" />
                </figure>
                <strong>Take our free practice test to help you choose the right course.</strong>
                <a href={`${siteDomain}/practice-tests/`} className="btn-blue-outline mb-20">Take free test</a>
            </div>
        </section>
    )
}

export default PracticeTestBanner;