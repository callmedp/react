import React from 'react';
import { Link } from 'react-router-dom';
import './skillGain.scss'

const SkillGain = (props) => {
    return (
        <section className="m-container mt-0 mb-0 pb-0">
            <div className="d-flex">
                <div className="m-skill-gain">
                    <h2 className="m-heading2">Skills you will gain</h2>
                    <ul className="m-skill-gain__list">
                        <li>Light</li>
                        <li>PythonR</li>
                        <li>Programming</li>
                        <li>Tableau</li>
                        <li>Data Science</li>
                        <li>Deep Learning</li>
                        <li>Data Visualization</li>
                        <li>Statistical computing</li>
                        <li>Visual Analytics</li>
                        <li>Dashboards</li>
                    </ul>
                    <div className="m-skill-gain__banner mt-30">
                        <p>Take our free practice test to test your skill level in <strong>Digital Marketing</strong></p>
                        <Link className="btn-blue-outline" to={"#"}>Take free test</Link>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;