import React from 'react';
import './keyFeatures.scss'

const KeyFeatures = (props) => {
    const { prd_uget } = props;

    return (
        <section className="m-container mt-0 mb-0" data-aos="fade-up">
            <div className="m-key-features">
                <h2 className="m-heading2">Key Features</h2>
                <p dangerouslySetInnerHTML={{__html: prd_uget}} />
                {/* <ul>
                    <li>Live Instructor-led Sessions(78 hrs)</li>
                    <li>Training Content(Presentations & Videos)</li>
                    <li>Get Q & A Support (for all learners at shine learning)</li>
                    <li>Get Placement Assistance after completion of course</li>
                    <li>Certified candidate gets 1 month complimentary featured profile</li>
                    <li>Get Q & A Support (for all learners at shine learning)</li>
                </ul> */}
            </div>
        </section>
    )
}


export default KeyFeatures;