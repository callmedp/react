import React from 'react';
import { imageUrl } from 'utils/domains';
import './practiceTestBanner.scss';
import { siteDomain } from 'utils/domains';

const PracticeTestBanner = (props) => {


    const testRedirection = () => {
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