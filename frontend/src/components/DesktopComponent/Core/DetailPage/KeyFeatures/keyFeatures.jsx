import React from 'react';
import './keyFeatures.scss';
import WhatYouGet from './whatYouGet';

const KeyFeatures = (props) => {
    const {prd_uget, pTF, prd_vendor_slug} = props;

    return (
        <section id="keyfeatures" className="container-fluid mb-0">
            <div className="row">
                <div className="container">
                    <div className="key-features">
                        <h2 className="heading2">Key Features</h2>
                        <p className="mt-20 mb-0" dangerouslySetInnerHTML={{__html: prd_uget}}></p>
                    </div>
                </div>
            </div>
            <br/>
            { pTF === 16 && <WhatYouGet prd_vendor_slug={prd_vendor_slug} /> }
        </section>
    )
}


export default KeyFeatures;