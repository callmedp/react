import React from 'react';
import './aboutSection.scss';

const AboutSection = (props) => {
    const { completeDescription } = props;

    return (
        <section id="aboutsection" className="container-fluid mt-0 mb-0">
            <div className="row">
                <div className="container">
                    <div className="about-section">
                        <h2 className="heading2">About</h2>
                        <p dangerouslySetInnerHTML={{__html:completeDescription}} />
                    </div>
                </div>
            </div>
            <br/>
        </section>
    )
}


export default AboutSection;