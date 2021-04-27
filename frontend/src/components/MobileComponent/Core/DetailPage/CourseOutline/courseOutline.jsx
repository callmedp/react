import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../FAQ/faq-detail.scss';

const CourseOutline = (props) => {

    const { chapter_list } = props;
    const [checkedId, setCheckedId] = useState(null);

    const accordionHandle = (index) => { (index === checkedId) ? setCheckedId(null) : setCheckedId(index) }

    return( 
        <section className="m-container m-faq-detail m-faq-outline m-lightblue-bg  mt-0 mb-0" id="m-faq" data-aos="fade-up">
            <h2 className="m-heading2">Course Outline</h2>
            <div className="tabs">
                {
                    chapter_list?.map((chap, index) => {
                        return (
                            <div className="tab" key={index} >
                                {
                                    !!chap.content && 
                                        <input type="radio" name="rd" id={"co" + index} checked = { checkedId === index } onClick={() => accordionHandle(index)}/>
                                }
                                <label className={`tab-label ${!!chap.content ? " " : 'no-dd'}`} htmlFor={ "co" + index } itemProp="name"><h3>{chap.heading}</h3></label>
                                {
                                    !!chap.content && 
                                        <div id="0" className="tab-content">
                                            <p itemProp="text" hidden="" dangerouslySetInnerHTML={{__html: chap.content}}/>
                                        </div>
                                }
                            </div>
                        )
                    })
                }
                {/* <div className="tab">
                    <input type="radio" id="co0" name="rd"/><label className="tab-label" htmlFor="co0" itemProp="name"><h3>Who will write my resume?</h3></label>
                    <div id="0" className="tab-content">
                        <p itemProp="text" hidden="">1 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                    </div>
                </div>
                <div className="tab">
                    <input type="radio" id="co1" name="rd"/><label className="tab-label" htmlFor="co1" itemProp="name"><h3>How to choose a resume format?</h3></label>
                    <div id="1" className="tab-content">
                        <p itemProp="text" hidden="">2 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                    </div>
                </div>
                <div className="tab">
                    <input type="radio" id="co2" name="rd"/><label className="tab-label" htmlFor="co2" itemProp="name"><h3>Why are resume formats important?</h3></label>
                    <div id="2" className="tab-content">
                        <p itemProp="text" hidden="">3 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                    </div>
                </div>
                <div className="tab">
                    <input type="radio" id="co3" name="rd"/><label className="tab-label" htmlFor="co3" itemProp="name"><h3>What makes a resume good and attractive?</h3></label>
                    <div id="3" className="tab-content">
                        <p itemProp="text" hidden="">4 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                    </div>
                </div> */}
                </div>
            </section>
        )
    }

export default CourseOutline;