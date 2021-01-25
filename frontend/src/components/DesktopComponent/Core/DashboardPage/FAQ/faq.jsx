import React, {useEffect} from 'react';
import Accordion from 'react-bootstrap/Accordion';
import '../../SkillPage/FAQ/faq.scss';
import FaqAccordion from '../../../Common/FaqAccordion/faqAccordion';
import {faqList} from '../../../../../utils/dashboardUtils/faqListUtils';

const FAQ = (props) => {
    const { setHasFaq } = props;

    useEffect(()=>{
        setHasFaq( faqList.length > 0 )
    },[])

    return (
        <section className="container-fluid lightgrey-bg mt-40" id="Faq">
            { faqList.length > 0 ?
                <div className="row">
                    <div className="container">
                        <h2 className="heading2 mt-40 text-center">Frequently Asked Questions</h2>
                        <div className="faq d-flex col-10 m-auto">
                            <div className="faq__list">
                                <Accordion defaultActiveKey="0">
                                    {
                                        faqList.map((item, index) => <FaqAccordion item={item} index={index}/>)   
                                    }
                                </Accordion>
                            </div>
                        </div>
                    </div>
                </div>
                : null 
            }
        </section>
    )
}

export default FAQ;