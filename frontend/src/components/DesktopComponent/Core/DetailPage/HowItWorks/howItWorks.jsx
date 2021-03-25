import React from 'react';
import './howItWorks.scss';
import { Link as LinkScroll } from 'react-scroll';

const HowItWorks = (props) => {
    const {dlvry_flow: {articles, main_heading}} = props;

    return (
        <section id="howitworks" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-40">
                    <div className="how-works">
                        <h2 className="heading2 text-center">{main_heading}?</h2>
                        <ul className="mt-30">
                            {
                                articles?.map((art, indx) => {
                                    return (
                                        <li key={indx}>
                                            <figure className="icon-how-works">
                                                <i className={`icon-how-works${indx+1}`}></i>
                                            </figure>
                                            <strong className="">{art.heading}</strong>
                                            <p>{art.article}</p>
                                        </li>
                                    )
                                })
                            }
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