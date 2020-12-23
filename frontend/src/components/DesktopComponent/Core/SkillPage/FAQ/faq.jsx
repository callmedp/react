import React, { useState } from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import './faq.scss'
import { useSelector } from 'react-redux';
import { imageUrl } from 'utils/domains';



const renderAccordion = (item, index) => {
    return (
        <Card key={index.toString() + item.heading}>
            <Accordion.Toggle as={Card.Header} eventKey={index === 0 ? '0' : index}>
                <p dangerouslySetInnerHTML={{__html : item.heading}}></p>
            </Accordion.Toggle>
            <Accordion.Collapse eventKey={index === 0 ? '0' : index}>
                <Card.Body dangerouslySetInnerHTML={{ __html: item.content }}>
                </Card.Body>
            </Accordion.Collapse>
        </Card>
)}


const FAQ = (props) => {

    const { faqList } = useSelector(store => store.skillBanner)
    const [sliceFlag, setSliceFlag] = useState(true)

    const loadMore = () => {
        setSliceFlag(state => !state)
    }
    
    return (
        faqList.length ? (
            <section className="container-fluid lightblue-bg mt-40" id="faq">
                <div className="row">
                    <div className="container">
                        <h2 className="heading2 mt-40">Frequently Asked Questions</h2>
                        <div className="faq d-flex">
                            <div className="faq__list">
                                <Accordion defaultActiveKey="0" >
                                    {
                                    (sliceFlag ? faqList.slice(0, 4) : faqList).map(renderAccordion)   
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
        ): null
    )
}

export default FAQ; 