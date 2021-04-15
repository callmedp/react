import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './faq-detail.scss';
import { MyGA } from 'utils/ga.tracking.js';

const FAQ = (props) => {

    const { faq_list } = props;
    const [sliceFlagFaq, setSliceFlagFaq] = useState(true)
    const [checkedIdFaq, setCheckedIdFaq] = useState(null);

    const accordionHandle = (index) => { (index === checkedIdFaq) ? setCheckedIdFaq(null) : setCheckedIdFaq(index) }

    const renderAccordion = (item, index) => {
        return (
            <div className="tab" key={index.toString() + item.question}>
                <input type="radio" id={"rd" + (index + 1000)} name={"rd" + (index + 1000)} checked = { checkedIdFaq === (index + 1000) } onClick={() => accordionHandle(index + 1000)}/><label className="tab-label" htmlFor={ "rd" + (index + 1000) } itemProp="name">{item.question}</label>
                <div id={index + 1000} className="tab-content">
                    <p itemProp="text" hidden="" dangerouslySetInnerHTML={{__html : item.answer}} />
                </div>
            </div>
        )
    }

    const loadMore = () => {
        MyGA.SendEvent('SkillMoreFAQs','ln_FAQ_click', 'more_FAQs', 'ln_FAQ','', false, true);
        setSliceFlagFaq(state => !state);
    }

    return(
        faq_list.length ? (
            <section className="m-container m-faq-detail lightblue-bg mt-0 mb-0" id="faq" data-aos="fade-up">
                <h3 className="m-heading2">Frequently Asked Questions</h3>
                    <div className="tabs">
                        { (sliceFlagFaq ? faq_list?.slice(0, 4) : faq_list).map(renderAccordion) }
                        { sliceFlagFaq && (faq_list?.length  > 4) ? <Link onClick={loadMore} to={"#"} className="m-load-more mt-20">Load More FAQS</Link> : '' }
                    </div>
            </section>
            ): null
    )

        // return(
        //     <section className="m-container m-faq-detail m-lightblue-bg mt-0 mb-0" id="m-faq" data-aos="fade-up">
        //         <h2 className="m-heading2">Frequently Asked Questions</h2>
        //         <div className="tabs">
        //             <div className="tab">
        //                 <input type="radio" id="rd0" name="rd"/><label className="tab-label" for="rd0" itemProp="name">Who will write my resume?</label>
        //                 <div id="0" className="tab-content">
        //                     <p itemProp="text" hidden="">A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
        //                 </div>
        //             </div>
        //             <div className="tab">
        //                 <input type="radio" id="rd1" name="rd"/><label className="tab-label" for="rd1" itemProp="name">How to choose a resume format?</label>
        //                 <div id="1" className="tab-content">
        //                     <p itemProp="text" hidden="">A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
        //                 </div>
        //             </div>
        //             <div className="tab">
        //                 <input type="radio" id="rd2" name="rd"/><label className="tab-label" for="rd2" itemProp="name">Why are resume formats important?</label>
        //                 <div id="2" className="tab-content">
        //                     <p itemProp="text" hidden="">A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
        //                 </div>
        //             </div>
        //             <div className="tab">
        //                 <input type="radio" id="rd3" name="rd"/><label className="tab-label" for="rd3" itemProp="name">What makes a resume good and attractive?</label>
        //                 <div id="3" className="tab-content">
        //                     <p itemProp="text" hidden="">A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
        //                 </div>
        //             </div>
        //             <Link to={"#"} className="m-load-more mt-20">Load More FAQS</Link>
        //         </div>
        //     </section>
        // )
    }

export default FAQ;