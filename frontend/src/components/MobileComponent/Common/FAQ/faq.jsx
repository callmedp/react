import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './faq.scss';
import { MyGA } from 'utils/ga.tracking.js';


const FAQ = (props) => {
    const faqList = props.faqList;
    const [sliceFlag, setSliceFlag] = useState(true)
    const [checkedId, setCheckedId] = useState(null);

    const accordionHandle = (index) => { (index === checkedId) ? setCheckedId(null) : setCheckedId(index) }

    const renderAccordion = (item, index) => {
        return (
            <div className="m-tab" key={index.toString() + item.heading} itemScope itemProp="mainEntity" itemType="https://schema.org/Question" >
                <input type="radio" id={"rd"+index} name="rd" checked = { checkedId === index } onClick={() => accordionHandle(index)} readOnly/><label className="m-tab-label" htmlFor={"rd"+index} ><span itemProp="name" dangerouslySetInnerHTML={{__html : item.heading}}/></label>
                <div id={index} className="m-tab-content" itemScope itemProp="acceptedAnswer" itemType="https://schema.org/Answer">
                    <p  hidden=""><span itemProp="text" dangerouslySetInnerHTML={{__html : item.content}}/></p>
                </div>
            </div>
    )}

    const loadMore = () => {
        // MyGA.SendEvent('SkillMoreFAQs', 'ln_FAQ_click', 'more_FAQs', 'ln_FAQ','', false, true);
        setSliceFlag(state => !state);
    }

    return(
        faqList.length ? (
            <div className="m-container m-faq" id="m-faq" itemScope itemType="https://schema.org/FAQPage">
                <h2 className="m-heading2" itemProp="name">Frequently Asked Questions</h2>
                <div className="m-tabs">
                    { (sliceFlag ? faqList.slice(0, 4) : faqList).map(renderAccordion) }
                    { sliceFlag && (faqList?.length  > 4) ? <Link onClick={loadMore} to={"#"} className="m-load-more mt-20">Load More FAQS</Link> : '' }
                </div>
            </div>): null
    )
}

export default FAQ;