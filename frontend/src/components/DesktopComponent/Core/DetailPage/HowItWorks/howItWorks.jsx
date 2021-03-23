import React from 'react';
import './howItWorks.scss';
import { Link as LinkScroll } from 'react-scroll';

const HowItWorks = (props) => {
    
    return (
        <section id="howitworks" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-40">
                    <div className="how-works">
                        <h2 className="heading2 text-center">How it will work?</h2>
                        <ul className="mt-30">
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works1"></i>
                                </figure>
                                <strong className="">Introduce yourself</strong>
                                <p>Place order and upload your initial resume</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works2"></i>
                                </figure>
                                <strong>We Update</strong>
                                <p>Our expert will update your profile</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works3"></i>
                                </figure>
                                <strong>Featured</strong>
                                <p>Get featured on shine</p>
                            </li>
                            <li>
                                <figure className="icon-how-works">
                                    <i className="icon-how-works4"></i>
                                </figure>
                                <strong>View</strong>
                                <p>Get 10x recruiter views</p>
                            </li>
                        </ul>
                        <div className="d-flex justify-content-center mt-50">
                            <LinkScroll to={"enquire-now"} className="btn btn-outline-primary btn-custom">Enquire now</LinkScroll>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default HowItWorks;