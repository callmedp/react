import React, { useEffect } from 'react';
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button';
import './skillGain.scss';
import { useSelector } from 'react-redux';
import { siteDomain, imageUrl } from 'utils/domains';

const SkillGain = (props) => {

    const { skillGainList, name, slug } = useSelector( store => store.skillBanner )
  
    const testRedirect = () => window.location.replace(`${siteDomain}/practice-tests/${slug}/sub`)

    return (
        <section className="container-fluid lightblue-bg mt-40" id="skGain" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="d-flex">
                        <div className="skill-gain">
                            <h2 className="heading2 mt-40">Skills you will gain</h2>
                            <div className="skill-gain__list">
                                {
                                    skillGainList?.map((skill, index) => {
                                        return (<React.Fragment key={index}>
                                            <Badge pill  variant="light">{skill}</Badge>&nbsp;
                                        </React.Fragment>)
                                    })
                                }   
                            </div>
                            <div className="skill-gain__banner mt-30  mb-30">
                                <p>Take our free practice test to test your skill level in <strong>{name}</strong></p>
                                <Button onClick={testRedirect} variant="outline-primary" className="ml-auto">TAKE FREE TEST</Button>&nbsp;
                            </div>
                        </div>

                        <figure className="skill-gain__img mt-40">
                            <span className="skill-tween1">
                                <img src={`${imageUrl}desktop/skill-tween1.svg`} />
                            </span>
                            <span className="skill-tween2">
                                <img src={`${imageUrl}desktop/skill-tween2.svg`} />
                            </span>
                            <span className="skill-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                <img src={`${imageUrl}desktop/skill-tween3.svg`} alt="Skills you will gain" />
                            </span>
                            <span className="skill-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                <img src={`${imageUrl}desktop/skill-tween4.svg`} alt="Skills you will gain" />
                            </span>
                            <span className="skill-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                <img src={`${imageUrl}desktop/skill-tween5.svg`} alt="Skills you will gain" />
                            </span>
                            <span className="skill-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700">
                                <img src={`${imageUrl}desktop/skill-tween6.svg`} alt="Skills you will gain" />
                            </span>
                            <span className="skill-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="800">
                                <img src={`${imageUrl}desktop/skill-tween7.svg`} alt="Skills you will gain" />
                            </span>
                            <span className="skill-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900">
                                <img src={`${imageUrl}desktop/skill-tween8.svg`} alt="Skills you will gain" />
                            </span>
                        </figure>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;