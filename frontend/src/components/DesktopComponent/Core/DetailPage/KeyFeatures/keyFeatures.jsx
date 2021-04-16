import React from 'react';
import './keyFeatures.scss';

const KeyFeatures = (props) => {
    const {prd_uget} = props;

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
        </section>
    )
}


export default KeyFeatures;