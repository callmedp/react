import React from 'react';
import { imageUrl } from 'utils/domains';
import './practiceTestBanner.scss';
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const PracticeTestBanner = (props) => {
    const sendLearningTracking = useLearningTracking();


    const testRedirection = () => {
        MyGA.SendEvent('ln_new_homepage','ln_free_test', 'ln_free_test','test_click', '',false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_practice_test_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'practice_test',
            eventCategory: ``,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })

        window.location.replace(`${siteDomain}/practice-tests/`);
    }

    return(
        <section className="container-fluid">
            <div className="row">
                <div className="container">
                    <div className="col-sm-12">
                        <div className="practice-test" data-aos="fade-up">
                            <figure>
                                <img src={`${imageUrl}desktop/practice-test-bg.png`} className="img-fluid" alt="Practice Test" />
                            </figure>
                            <strong>Take our free practice test to help you choose the right course.</strong>
                            <button type="button" onClick={ testRedirection } className="btn btn-outline-primary mr-30">TAKE FREE TEST</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default PracticeTestBanner;