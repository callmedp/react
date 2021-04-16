import React from 'react';
import './keyFeatures.scss'
import WhatYouGet from './whatYouGet';

const KeyFeatures = (props) => {
    const { prd_uget, typeFlow, prd_vendor_slug } = props;

    return (
        <>
            <section id="features" className="m-container mt-0 mb-0" data-aos="fade-up">
                <div className="m-key-features">
                    <h2 className="m-heading2">Key Features</h2>
                    <p dangerouslySetInnerHTML={{__html: prd_uget}} />
                </div>
            </section>
            { 
                typeFlow === 16 && 
                    <WhatYouGet prd_vendor_slug={prd_vendor_slug} />
            }
        </>
    )
}


export default KeyFeatures;