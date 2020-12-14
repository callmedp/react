import React from 'react';
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button';
import './skillGain.scss';
import { useSelector } from 'react-redux';
import { siteDomain, imageUrl } from 'utils/domains';

const SkillGain = (props) => {

    const { skillGainList, name, slug } = useSelector( store => store.skillBanner )
  
    const testRedirect = () => window.location.replace(`${siteDomain}/practice-tests/${slug}/sub`)

    return (
        <section className="container-fluid lightblue-bg mt-40" id="skGain">
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
                            <img src={`${imageUrl}desktop/skill-gain-bg.svg`} alt="Skills you will gain" />
                        </figure>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;