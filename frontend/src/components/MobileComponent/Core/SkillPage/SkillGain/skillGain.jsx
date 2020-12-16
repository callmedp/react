import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import './skillGain.scss'
import { Button } from 'react-bootstrap';
import { siteDomain } from 'utils/domains';

const SkillGain = (props) => {
    const { skillGainList, name, slug } = useSelector( store => store.skillBanner )
    const testRedirect = () => window.location.href = `${siteDomain}/practice-tests/${slug}/sub`;

    return (
        <section className="m-container mt-0 mb-0 pb-0">
            <div className="d-flex">
                <div className="m-skill-gain">
                    <h2 className="m-heading2">Skills you will gain</h2>
                    <ul className="m-skill-gain__list">
                        {
                            skillGainList?.map((skill, index) => {
                                return <li key={index}>{skill}</li>
                            })
                        } 
                    </ul>
                    <div className="m-skill-gain__banner mt-30">
                        <p>Take our free practice test to test your skill level in <strong>{name}</strong></p>
                        <Button className="btn-blue-outline" onClick={testRedirect}>Take free test</Button>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;