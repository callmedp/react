import React, {useState} from 'react';
import './sampleCertificate.scss';
import {Link} from 'react-router-dom';
import { imageUrl } from 'utils/domains';

const SampleCertificate = (props) => {
    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="m-sample-certificate">
                <h2 className="m-heading2">Sample certificate</h2>
                <Link to={"#"}>
                    <figure>
                        <img src={`${imageUrl}/mobile/sample-certificate-thumb.jpg`} alt="Sample certificate" />
                        <span variant="primary">View</span>
                    </figure>
                </Link>
            </div>
        </section>
    )
}


export default SampleCertificate;