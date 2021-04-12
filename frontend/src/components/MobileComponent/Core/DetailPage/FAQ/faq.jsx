import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './faq-detail.scss';

const FAQ = (props) => {

    const { faq_list } = props;
    const [sliceFlag, setSliceFlag] = useState(true)
    const [checkedId, setCheckedId] = useState(null);

    const accordionHandle = (index) => { (index === checkedId) ? setCheckedId(null) : setCheckedId(index) }

    const renderAccordion = (item, index) => {
        return (
            <div className="tab" key={index.toString() + item.question}>
                <input type="radio" id={"rd" + index} name="rd" checked = { checkedId === index } onClick={() => accordionHandle(index)}/><label className="tab-label" htmlFor={ "rd" + index } itemProp="name">{item.question}</label>
                <div id={index} className="tab-content">
                    <p itemProp="text" hidden="" dangerouslySetInnerHTML={{__html : item.answer}} />
                </div>
            </div>
        )
    }

    const loadMore = () => {
        setSliceFlag(state => !state);
    }

    return(
        faq_list.length ? (
            <section className="m-container m-faq-detail m-lightblue-bg mt-0 mb-0" id="faq" data-aos="fade-up">
                <h2 className="m-heading2">Frequently Asked Questions</h2>
                    <div className="tabs">
                        { (sliceFlag ? faq_list?.slice(0, 4) : faq_list).map(renderAccordion) }
                        { sliceFlag && (faq_list?.length  > 4) ? <Link onClick={loadMore} to={"#"} className="m-load-more mt-20">Load More FAQS</Link> : '' }
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