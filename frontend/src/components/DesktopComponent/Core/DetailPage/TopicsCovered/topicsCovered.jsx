import React from 'react';
import './topicsCovered.scss';

const TopicsCovered = (props) => {
    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="topic-covered">
                        <h2 className="heading2 mt-10">Topics covered</h2>
                        <ul className="mt-30 mb-0">
                            <li>PythonR</li>
                            <li>Programming</li>
                            <li>Tableau</li>
                            <li>Data Science</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}


export default TopicsCovered;