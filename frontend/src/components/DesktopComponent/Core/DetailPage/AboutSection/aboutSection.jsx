import React from 'react';
import './aboutSection.scss';

const AboutSection = (props) => {
    const { product_detail } = props;

    return (
        <>
            {
                product_detail?.prd_about &&
                    <section id="aboutsection" className="container-fluid mt-0 mb-0" data-aos="fade-up">
                        <div className="row">
                            <div className="container">
                                <div className="about-section">
                                    <h2 className="heading2">Overview</h2>
                                    <p dangerouslySetInnerHTML={{__html:product_detail.prd_about}} />
                                </div>
                            </div>
                        </div>
                        <br/>
                    </section>
            }

            {
                product_detail?.prd_desc &&
                    <section id="aboutsection" className="container-fluid mt-0 mb-0" data-aos="fade-up">
                        <div className="row">
                            <div className="container">
                                <div className="about-section">
                                    <h2 className="heading2">About</h2>
                                    <p dangerouslySetInnerHTML={{__html:product_detail.prd_desc}} />
                                </div>
                            </div>
                        </div>
                        <br/>
                    </section>
            }
        </>
    )
}


export default AboutSection;