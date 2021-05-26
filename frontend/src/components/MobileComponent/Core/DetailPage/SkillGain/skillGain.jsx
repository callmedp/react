import React from 'react';
import { Link } from 'react-router-dom';
import '../../SkillPage/SkillGain/skillGain.scss';

const SkillGain = (props) => {
    const { skills } = props
    window['course_skills'] = skills.slice(0,4);
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
                    </ul>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;