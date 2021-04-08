import React from 'react';
import './topicsCovered.scss'

const TopicsCovered = (props) => {
    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-topics-covered">
                <h2 className="m-heading2 mb-10">Topics Covered</h2>
                <ul>
                    <li>PythonR</li>
                    <li>Programming</li>
                    <li>Tableau</li>
                    <li>Data Science</li>
                </ul>
            </div>
        </section>
    )
}


export default TopicsCovered;