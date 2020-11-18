import React from 'react';
import Badge from 'react-bootstrap/Badge';
import { Link } from 'react-router-dom';
import './otherSkills.scss'

const OtherSkills = (props) => {
    return (
        <section className="container-fluid lightblue-bg mt-40">
            <div className="row">
                <div className="container">
                        <div className="other-skills">
                            <h2 className="heading2 mt-40">Other Skills To Explore</h2>
                            <div className="other-skills__list">
                                <Badge pill variant="light"><Link to={"#"}>Sales Courses & Certifications</Link></Badge>{' '}
                                <Badge pill variant="light"><Link to={"#"}>Retail Courses & Certifications</Link></Badge>{' '}
                                <Badge pill variant="light"><Link to={"#"}>Product Marketing</Link></Badge>{' '}
                                <Badge pill variant="light"><Link to={"#"}>Service Marketing</Link></Badge>{' '}
                            </div>

                        </div>

                </div>
            </div>
        </section>
    )
}

export default OtherSkills;