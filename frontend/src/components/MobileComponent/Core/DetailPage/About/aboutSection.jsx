import React from 'react';
import './aboutSection.scss'

const About = (props) => {
    const { desc } = props;

    return (
        <>
            <section id="features" className="m-container mt-0 mb-0" data-aos="fade-up">
                <div className="m-about-section">
                    <h2 className="m-heading2">About</h2>
                    <p dangerouslySetInnerHTML={{__html: desc}} />
                </div>
            </section>
        </>
    )
}


export default About;