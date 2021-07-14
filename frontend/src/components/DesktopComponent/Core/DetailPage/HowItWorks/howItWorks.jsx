import React from 'react';
import './howItWorks.scss';
import { Link as LinkScroll } from 'react-scroll';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const HowItWorks = (props) => {
    const {dlvry_flow: {articles, main_heading}, prd_H1, product_id} = props;
    const sendLearningTracking = useLearningTracking();

    const trackEnquireNow = () => {
        sendLearningTracking({
            productId: '',
            event: `course_detail_how_it_works_${stringReplace(prd_H1)}_${product_id}_enquire_now_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'how_it_works',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

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
                            <LinkScroll to={"enquire-now"} onClick={trackEnquireNow} className="btn btn-outline-primary btn-custom" offset={-160}>Enquire now</LinkScroll>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default HowItWorks;