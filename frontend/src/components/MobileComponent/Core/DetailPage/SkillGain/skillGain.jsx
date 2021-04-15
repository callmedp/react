import React from 'react';
import { Link } from 'react-router-dom';
import '../../SkillPage/SkillGain/skillGain.scss';

const SkillGain = (props) => {
    const { skills } = props
    
    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <div className="m-skill-gain">
                    <h3 className="m-heading2">Skills you will gain</h3>
                    <ul className="m-skill-gain__list">
                        {
                            skills?.map((skill, index) => {
                                return (
                                    <li key={index}>{skill}</li>
                                )
                            })
                        }
                        {/* <li>Light</li>
                        <li>PythonR</li>
                        <li>Programming</li>
                        <li>Tableau</li>
                        <li>Data Science</li>
                        <li>Deep Learning</li>
                        <li>Data Visualization</li>
                        <li>Statistical computing</li>
                        <li>Visual Analytics</li>
                        <li>Dashboards</li> */}
                    </ul>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;