import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './faq-detail.scss';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const FAQ = (props) => {

    const { faq_list } = props;
    const [sliceFlagFaq, setSliceFlagFaq] = useState(true)
    const [checkedIdFaq, setCheckedIdFaq] = useState(null);
    const sendLearningTracking = useLearningTracking();
    const regex = /(<([^>]+)>)/ig;

    const accordionHandle = (index) => { (index === checkedIdFaq) ? setCheckedIdFaq(null) : setCheckedIdFaq(index) }

    const renderAccordion = (item, index) => {
        return (
            <div className="tab" key={index.toString() + item.question} itemScope 
            itemType="https://schema.org/Question">
                <input type="radio" id={"rd" + (index + 1000)} name={"rd" + (index + 1000)} checked = { checkedIdFaq === (index + 1000) } onClick={() => accordionHandle(index + 1000)}/><label className="tab-label" onClick={() => courseFaqTracking(item.question, index) } htmlFor={ "rd" + (index + 1000) } itemProp="name">{item.question}</label>
                <div id={index + 1000} className="tab-content" itemProp="acceptedAnswer" itemScope itemType="https://schema.org/Answer">
                    <p itemProp="text" hidden="" dangerouslySetInnerHTML={{__html : item.answer}} />
                </div>
            </div>
        )
    }

    const courseFaqTracking = (question, indx) => {
        MyGA.SendEvent('FAQs','ln_FAQ_click', 'ln_down_arrow_click', 'ln_'+ stringReplace(question.replace(regex, '')),'', false, true);

        sendLearningTracking({
            productId: '',
            event: `course_detail_faq_${stringReplace(question)}_${indx}_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'faqs',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    const loadMore = () => {
        MyGA.SendEvent('SkillMoreFAQs','ln_FAQ_click', 'more_FAQs', 'ln_FAQ','', false, true);
        setSliceFlagFaq(state => !state);
        
        sendLearningTracking({
            productId: '',
            event: `course_detail_load_more_faqs_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'faqs',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        faq_list.length ? (
            <section className="m-container m-faq-detail lightblue-bg mt-0 mb-0" id="faq" data-aos="fade-up">
                <h3 className="m-heading2">Frequently Asked Questions</h3>
                    <div className="tabs">
                        { (sliceFlagFaq ? faq_list?.slice(0, 4) : faq_list).map(renderAccordion) }
                        { sliceFlagFaq && (faq_list?.length  > 4) ? <Link onClick={loadMore} to={"#"} className="m-load-more mt-20">Load More FAQS</Link> : '' }
                    </div>
            </section>
            )
        : null
    )
}

export default FAQ;