import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './faq.scss';
import { useSelector } from 'react-redux';

const renderAccordion = (item, index) => {
    return (
        <div className="tab" key={index.toString() + item.heading}>
            <input type="radio" id={"rd"+index} name="rd"/><label className="tab-label" htmlFor={"rd"+index} itemProp="name"><span dangerouslySetInnerHTML={{__html : item.heading}}/></label>
            <div id={index} className="tab-content">
                <p itemProp="text" hidden=""><span dangerouslySetInnerHTML={{__html : item.content}}/></p>
            </div>
        </div>
)}

const FAQ = (props) => {

    const { faqList } = useSelector(store => store.skillBanner)
    const [sliceFlag, setSliceFlag] = useState(true)

    const loadMore = () => {
        setSliceFlag(state => !state)
    }
    return(
        faqList.length ? (
            <div className="m-container m-faq" id="m-faq">
                <h2 className="m-heading2">Frequently Asked Questions</h2>
                <div className="tabs">
                    { (sliceFlag ? faqList.slice(0, 4) : faqList).map(renderAccordion) }
                    { sliceFlag ? <Link onClick={loadMore} to={"#"} className="m-load-more mt-20">Load More FAQS</Link> : '' }
                </div>
            </div>): null
    )
}

export default FAQ;