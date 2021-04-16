import React from 'react';
import './keyFeatures.scss'

const KeyFeatures = (props) => {
    const { prd_uget } = props;

    return (
        <>
            <section id="features" className="m-container mt-0 mb-0" data-aos="fade-up">
                <div className="m-key-features">
                    <h2 className="m-heading2">Key Features</h2>
                    <p dangerouslySetInnerHTML={{__html: prd_uget}} />
                </div>
            </section>
            
        </>
    )
}


export default KeyFeatures;