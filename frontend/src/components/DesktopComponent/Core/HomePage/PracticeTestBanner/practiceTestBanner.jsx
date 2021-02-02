import React from 'react';
import './practiceTestBanner.scss';

const PracticeTestBanner = (props) => {
    return(
        <section className="container-fluid">
            <div className="row">
                <div className="container">
                    <div className="col-sm-12">
                        <div className="practice-test" data-aos="fade-up">
                            <figure>
                                <img src="./media/images/practice-test-bg.png" className="img-fluid" alt="Practice Test" />
                            </figure>
                            <strong>Take our free practice test to help you choose the right course.</strong>
                            <button type="button" className="btn btn-outline-primary mr-30">TAKE FREE TEST</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default PracticeTestBanner;