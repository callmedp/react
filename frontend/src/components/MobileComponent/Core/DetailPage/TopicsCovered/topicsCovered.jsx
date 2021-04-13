import React from 'react';
import './topicsCovered.scss'

const TopicsCovered = (props) => {
    const { chapter_list } = props;

    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up" id="topicsCovered">
            <div className="m-topics-covered">
                <h2 className="m-heading2 mb-10">Topics Covered</h2>
                <ul>
                    {
                        chapter_list?.map((chptr, idx) => {
                            return (
                                <li key={idx}>
                                    {chptr.heading}
                                </li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}


export default TopicsCovered;