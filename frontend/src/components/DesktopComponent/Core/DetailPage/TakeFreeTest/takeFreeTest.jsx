import React from 'react';
import './takeFreeTest.scss';
import { siteDomain } from 'utils/domains';

const TakeFreeTest = (props) => {
    
    const { should_take_test_url } = props

    const testRedirection = () => {
        window.location.replace(`${siteDomain}/practice-tests/${should_take_test_url}/sub`);
    }

    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="take-test-free">
                    <strong>Test your skills</strong>
                    <p>Take our free practice test to test your skill level in <strong>Digital Marketing</strong></p>
                    <button type="button" onClick={ testRedirection } className="btn btn-outline-primary">TAKE FREE TEST</button>
                </div>
            </div>
        </section>
    )
}

export default TakeFreeTest;