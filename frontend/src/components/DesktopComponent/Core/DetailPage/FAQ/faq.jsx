import React, { useState } from 'react';
import Accordion from 'react-bootstrap/Accordion';
import { Link } from 'react-router-dom';
import '../../SkillPage/FAQ/faq.scss';
import Card from 'react-bootstrap/Card';
import { MyGA } from 'utils/ga.tracking.js';
import { imageUrl } from 'utils/domains';

const FAQ = (props) => {
    const { faq_list } = props;
    const [sliceFlag, setSliceFlag] = useState(true);
    const regex = /(<([^>]+)>)/ig;

    const loadMore = () => {
        MyGA.SendEvent('SkillMoreFAQs','ln_FAQ_click', 'more_FAQs', 'ln_FAQ','', false, true);
        setSliceFlag(state => !state);
    }

    return (
        <section id="faqs" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <h2 className="heading2 mt-40">Frequently Asked Questions</h2>
                    <div className="faq d-flex">
                        <div className="faq__list">
                            <Accordion defaultActiveKey="0" >
                                {
                                    (sliceFlag ? faq_list.slice(0, 4) : faq_list).map((item, index) => 
                                        <Card data-aos="fade-up" key={index.toString() + item.question} itemScope itemProp="mainEntity" 
                                        itemType="https://schema.org/Question" >
                                            <Accordion.Toggle as={Card.Header} eventKey={index === 0 ? '0' : index} >
                                                <p className="font-weight-bold" dangerouslySetInnerHTML={{__html : item.question}} onClick={() => MyGA.SendEvent('FAQs','ln_FAQ_click', 'ln_down_arrow_click', 'ln_'+item.question.replace(regex, ''),'', false, true) }></p>
                                                <meta itemProp="name" content={item.question} />
                                            </Accordion.Toggle>
                                            <Accordion.Collapse eventKey={index === 0 ? '0' : index} itemProp="acceptedAnswer" itemScope 
                                                            itemType="https://schema.org/Answer">
                                                <Card.Body itemProp="text" dangerouslySetInnerHTML={{ __html: item.answer }}>
                                                </Card.Body>
                                            </Accordion.Collapse>
                                        </Card>
                                    )   
                                }
                            </Accordion>
                            { sliceFlag ? <Link onClick={loadMore} to={"#"} className="load-more pt-20">Load More FAQS</Link> : '' }
                        </div>
                        <div className="faq__img">
                            <span className="faq-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100">
                                <img src={`${imageUrl}desktop/faq-tween1.svg`} />
                            </span>
                            <span className="faq-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200">
                                <img src={`${imageUrl}desktop/faq-tween2.svg`} />
                            </span>
                            <span className="faq-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src={`${imageUrl}desktop/faq-tween3.svg`} />
                            </span>
                            <span className="faq-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                <img src={`${imageUrl}desktop/faq-tween4.svg`} />
                            </span>
                            <span className="faq-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                <img src={`${imageUrl}desktop/faq-tween5.svg`} />
                            </span>
                            <span className="faq-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                <img src={`${imageUrl}desktop/faq-tween6.svg`} />
                            </span>
                            <span className="faq-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src={`${imageUrl}desktop/faq-tween7.svg`} />
                            </span>
                            <span className="faq-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                <img src={`${imageUrl}desktop/faq-tween8.svg`} />
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FAQ;