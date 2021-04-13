import React from 'react';
import './topicsCovered.scss';

const TopicsCovered = (props) => {
    const { chapter_list } = props;

    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="topic-covered">
                        <h2 className="heading2 mt-10">Topics covered</h2>
                        <ul className="mt-30 mb-0">
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
                </div>
            </div>
        </section>
    )
}


export default TopicsCovered;