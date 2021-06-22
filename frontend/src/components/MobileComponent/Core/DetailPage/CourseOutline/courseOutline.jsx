import React, { useState } from 'react';
import '../FAQ/faq-detail.scss';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const CourseOutline = (props) => {
    const {chapter_list} = props;
    const sendLearningTracking = useLearningTracking();
    const [checkedId, setCheckedId] = useState(null);
    const accordionHandle = (index) => { (index === checkedId) ? setCheckedId(null) : setCheckedId(index) };

    const outlineTracking = (chap, indx) => {
        sendLearningTracking({
            productId: '',
            event: `course_detail_course_outline_${stringReplace(chap)}_${indx}_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'course_outline',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

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
                                <label onClick={() => outlineTracking(chap?.heading, index)} className={`tab-label ${!!chap.content ? " " : 'no-dd'}`} htmlFor={ "co" + index } itemProp="name"><h3>{chap.heading}</h3></label>
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
            </div>
        </section>
    )
}

export default CourseOutline;