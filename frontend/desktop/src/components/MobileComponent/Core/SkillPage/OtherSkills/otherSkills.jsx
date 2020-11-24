import React from 'react';
import { Link } from 'react-router-dom';
import './otherSkills.scss'

const OtherSkills = (props) => {
    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0">
            <div className="d-flex">
                <div className="m-other-skill">
                    <h2 className="m-heading2">Other Skills To Explore</h2>
                    <ul className="m-other-skill__list">
                        <li>
                            <Link to={"#"}>Sales Courses</Link>
                        </li>
                        <li>
                            <Link to={"#"}>Service Marketing</Link>
                        </li>
                        <li>
                            <Link to={"#"}>Retail Courses certification</Link>
                        </li>
                        <li>
                            <Link to={"#"}>Product Marketing</Link>
                        </li>
                    </ul>

                </div>
            </div>
        </section>
    )
}

export default OtherSkills;