import React from 'react';
import Badge from 'react-bootstrap/Badge';
import {Link} from 'react-router-dom';
import '../../SkillPage/SkillGain/skillGain';

const SkillGain = (props) => {
    
    return (
        <section className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="d-flex">
                        <div className="skill-gain">
                            <h2 className="heading2 mt-40">Skills you will gain</h2>
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
                            <div className="d-flex mt-50">
                                <Link to={"#"} className="btn btn-outline-primary btn-custom">Enquire now</Link>
                            </div>
                        </div>
                        <figure className="skill-gain__img mt-40">
                            <span className="skill-tween1">
                                <img src="/media/images/desktop/skill-tween1.svg" />
                            </span>
                            <span className="skill-tween2">
                                <img src="/media/images/desktop/skill-tween2.svg" />
                            </span>
                            <span className="skill-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                <img src="/media/images/desktop/skill-tween3.svg" />
                            </span>
                            <span className="skill-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                <img src="/media/images/desktop/skill-tween4.svg" />
                            </span>
                            <span className="skill-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                <img src="/media/images/desktop/skill-tween5.svg" />
                            </span>
                            <span className="skill-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700">
                                <img src="/media/images/desktop/skill-tween6.svg" />
                            </span>
                            <span className="skill-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="800">
                                <img src="/media/images/desktop/skill-tween7.svg" />
                            </span>
                            <span className="skill-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900">
                                <img src="/media/images/desktop/skill-tween8.svg" />
                            </span>
                        </figure>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;