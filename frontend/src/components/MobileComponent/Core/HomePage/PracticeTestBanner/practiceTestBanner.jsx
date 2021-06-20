import React from 'react';
import { siteDomain, imageUrl } from 'utils/domains';
import './practiceTestBanner.scss';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const PracticeTestBanner = () => {
    const sendLearningTracking = useLearningTracking();
    
    const testRedirection = () => {
        MyGA.SendEvent('ln_new_homepage','ln_free_test', 'ln_free_test','test_click', '',false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_practice_test_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'practice_test',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="m-practice-test m-lightblue-bg">
                <figure>
                    <img src={`${imageUrl}mobile/practice-test-bg.png`} className="img-fluid w-100" alt="Practice Test" />
                </figure>
                <strong>Take our free practice test to help you choose the right course.</strong>
                <a href={`${siteDomain}/practice-tests/`} onClick={ testRedirection }  className="btn-blue-outline mb-20">Take free test</a>
            </div>
        </section>
    )
}

export default PracticeTestBanner;