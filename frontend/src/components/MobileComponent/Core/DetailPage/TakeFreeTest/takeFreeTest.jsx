import React from 'react';
import './takeFreeTest.scss';
import { siteDomain } from 'utils/domains';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { useDispatch } from 'react-redux';

const TakeFreeTest = (props) => {
    const { should_take_test_url, test_title } = props;
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();

    const testRedirection = () => {
        dispatch(trackUser({"query" : tracking_data, "action" :'take_free_test'}));
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <div className="m-take-test-free">
                    <h2 className="m-heading2">Test your skills</h2>
                    <p>Take our free practice test to test your skill level in <strong>{test_title}</strong></p>
                    <a href={`${siteDomain}${should_take_test_url}`} onClick={ testRedirection } className="btn-blue-outline">Take free test</a>
                </div>
            </div>
        </section>
    )
}

export default TakeFreeTest;