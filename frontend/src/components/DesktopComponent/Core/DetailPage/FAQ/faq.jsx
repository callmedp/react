import React, { useState, useEffect } from 'react';
import Accordion from 'react-bootstrap/Accordion';
import { Link } from 'react-router-dom';
import '../../SkillPage/FAQ/faq.scss';
import FaqAccordion from '../../../Common/FaqAccordion/faqAccordion';
import Card from 'react-bootstrap/Card';

const FAQ = (props) => {
    const { faq_list } = props;
    // console.log(props)
    const [sliceFlag, setSliceFlag] = useState(true);

    const loadMore = () => {
        setSliceFlag(state => !state);
    }

    return (
        <section id="faqs" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <h2 className="heading2 mt-40">Frequently Asked Questions</h2>
                    <div className="faq d-flex">
                        <div className="faq__list">
                            <Accordion defaultActiveKey="0">
                                {/* {
                                    (sliceFlag ? faq_list.slice(0, 4) : faq_list).map((item, index) => <FaqAccordion item={item} index={index}/>)   
                                } */}
                                {faq_list?.map((faqs, indx) => {
                                    return (
                                        <Card data-aos="fade-up" key={indx}>
                                            <Accordion.Toggle as={Card.Header} eventKey={indx}>
                                            <strong>{faqs.question}</strong>
                                            </Accordion.Toggle>
                                            <Accordion.Collapse eventKey={indx}>
                                            <Card.Body>{faqs.answer}</Card.Body>
                                            </Accordion.Collapse>
                                        </Card>
                                    )
                                })}
                                {/* <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="0">
                                    <strong>What is a resume format?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="0">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="1">
                                    <strong>How to choose a resume format?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="1">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="2">
                                    <strong>Why are resume formats important?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="2">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="3">
                                    <strong>What makes a resume good and attractive?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="3">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="4">
                                    <strong>Why are resume formats important?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="4">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="5">
                                    <strong>What makes a resume good and attractive?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="5">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card> */}
                            </Accordion>
                            { sliceFlag ? <Link onClick={loadMore} to={"#"} className="load-more pt-20">Load More FAQS</Link> : '' }
                        </div>
                        <div className="faq__img">
                            <span className="faq-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100">
                                <img src="/media/images/desktop/faq-tween1.svg" />
                            </span>
                            <span className="faq-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200">
                                <img src="/media/images/desktop/faq-tween2.svg" />
                            </span>
                            <span className="faq-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src="/media/images/desktop/faq-tween3.svg" />
                            </span>
                            <span className="faq-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                <img src="/media/images/desktop/faq-tween4.svg" />
                            </span>
                            <span className="faq-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                <img src="/media/images/desktop/faq-tween5.svg" />
                            </span>
                            <span className="faq-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                <img src="/media/images/desktop/faq-tween6.svg" />
                            </span>
                            <span className="faq-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src="/media/images/desktop/faq-tween7.svg" />
                            </span>
                            <span className="faq-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src="/media/images/desktop/faq-tween8.svg" />
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FAQ;