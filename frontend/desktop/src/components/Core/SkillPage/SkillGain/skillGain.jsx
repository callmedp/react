import React from 'react';
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button'
import './skillGain.scss'

const SkillGain = (props) => {
    return (
        <section className="container-fluid lightblue-bg mt-40">
            <div className="row">
                <div className="container">
                    <div className="d-flex">
                        <div className="skill-gain">
                            <h2 className="mt-40">Skills you will gain</h2>
                            <div className="skill-gain__list">
                                <Badge pill variant="light">Light</Badge>{' '}
                                <Badge pill variant="light">PythonR</Badge>{' '}
                                <Badge pill variant="light">Programming</Badge>{' '}
                                <Badge pill variant="light">Tableau</Badge>{' '}
                                <Badge pill variant="light">Data Science</Badge>{' '}
                                <Badge pill variant="light">Deep Learning</Badge>{' '}
                                <Badge pill variant="light">Data Visualization</Badge>{' '}
                                <Badge pill variant="light">Statistical computing</Badge>{' '}
                                <Badge pill variant="light">Visual Analytics</Badge>{' '}
                                <Badge pill variant="light">Dashboards</Badge>{' '}
                            </div>
                            <div className="skill-gain__banner mt-30  mb-30">
                                <p>Take our free practice test to test your skill level in <strong>Digital Marketing</strong></p>
                                <Button variant="outline-primary" className="ml-auto">Take free test</Button>{' '}
                            </div>
                        </div>
                        <figure className="skill-gain__img mt-40">
                            <img src="./media/images/skill-gain-bg.svg" alt="Skills you will gain" />
                        </figure>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;