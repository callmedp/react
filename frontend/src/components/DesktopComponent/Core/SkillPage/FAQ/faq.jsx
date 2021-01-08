import React, { useState } from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import './faq.scss'
import { useSelector, connect } from 'react-redux';
import { imageUrl } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';



const FAQ = (props) => {

    const { faqList } = useSelector(store => store.skillBanner);
    const { setHasFaq } = props;
    const [sliceFlag, setSliceFlag] = useState(true);
    const regex = /(<([^>]+)>)/ig;

    const loadMore = () => {
        MyGA.SendEvent('SkillMoreFAQs','ln_FAQ_click', 'more_FAQs', 'ln_FAQ','', false, true);
        setSliceFlag(state => !state)
    }

    useEffect(()=>{
        setHasFaq( faqList.length > 0 )
    },[faqList])

    const renderAccordion = (item, index) => {
        
        return (
            <Card key={index.toString() + item.heading} >
                <Accordion.Toggle as={Card.Header} eventKey={index === 0 ? '0' : index} itemScope itemProp="mainEntity" 
                              itemType="https://schema.org/Question">
                    <p dangerouslySetInnerHTML={{__html : item.heading}} onClick={() => MyGA.SendEvent('SkillFAQs','ln_FAQ_click', 'ln_down_arrow_click', 'ln_'+item.heading.replace(regex, ''),'', false, true) }></p>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey={index === 0 ? '0' : index} itemScope 
                               itemProp="acceptedAnswer" itemType="https://schema.org/Answer">
                    <Card.Body dangerouslySetInnerHTML={{ __html: item.content }}>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
    )}
    
    return (
        faqList.length ? (
            <section className="container-fluid lightblue-bg mt-40" id="faq" data-aos="fade-up" itemScope itemType="https://schema.org/FAQPage">
                <div className="row">
                    <div className="container">
                        <h2 className="heading2 mt-40" itemProp="name">Frequently Asked Questions</h2>
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
                                <span className="faq-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween1.svg`} alt="faqs banner 1" />
                                </span>
                                <span className="faq-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween2.svg`} alt="faqs banner 2" />
                                </span>
                                <span className="faq-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween3.svg`} alt="faqs banner 3" />
                                </span>
                                <span className="faq-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween4.svg`} alt="faqs banner 4" />
                                </span>
                                <span className="faq-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween5.svg`} alt="faqs banner 5" />
                                </span>
                                <span className="faq-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween6.svg`} alt="faqs banner 6" />
                                </span>
                                <span className="faq-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween7.svg`} alt="faqs banner 7" />
                                </span>
                                <span className="faq-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                                    <img src={`${imageUrl}desktop/faq-tween8.svg`} alt="faqs banner 8" />
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        ): null
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "gaTrack": (data) => {
             MyGA.SendEvent(data)
        }
    }
}


export default connect(null, mapDispatchToProps)(FAQ);