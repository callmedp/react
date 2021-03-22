import React from 'react';
import { Link } from 'react-router-dom';
import './takeFreeTest.scss'
import { siteDomain } from 'utils/domains';

const TakeFreeTest = (props) => {
    
    const { should_take_test_url } = props

    const testRedirection = () => {
        window.location.replace(`${siteDomain}/practice-tests/${should_take_test_url}/sub`);
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <div className="m-take-test-free">
                    <h2 className="m-heading2">Test your skills</h2>
                    <p>Take our free practice test to test your skill level in <strong>Digital Marketing</strong></p>
                    <Link className="btn-blue-outline" to={"#"} onClick={ testRedirection } >Take free test</Link>
                </div>
            </div>
        </section>
    )
}

export default TakeFreeTest;