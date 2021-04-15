import React from 'react';
import './aboutSection.scss';

const AboutSection = (props) => {
    const {prd_uget, pTF, prd_vendor_slug} = props;

    return (
        <section id="aboutsection" className="container-fluid mt-0 mb-0">
            <div className="row">
                <div className="container">
                    <div className="about-section">
                        <h2 className="heading2">About</h2>
                        <p>Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt. Study with confidence as the course covers every topic in accordance with IASSC. Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge along with DMAIC problem solving approach.</p>
                    </div>
                </div>
            </div>
            <br/>
        </section>
    )
}


export default AboutSection;