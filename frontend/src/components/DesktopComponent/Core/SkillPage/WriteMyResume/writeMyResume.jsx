import React from 'react';
import Button from 'react-bootstrap/Button';
import './writeMyresume.scss';
import { resumeShineSiteDomain, imageUrl } from 'utils/domains';

const WriteMyResume = (props) => {

    const builderRedirect = () => window.location.replace(`${resumeShineSiteDomain}/resume-builder`)
    
    return (
        <section className="write-resume" data-aos="fade-up">
            <div className="write-resume__text">
                <strong className="heading3">Not getting enough calls from recruiters ?</strong>
                <p>Make your resume stand out by letting our experts write it for you</p>
                <Button onClick = {builderRedirect} variant="outline-primary" className="ml-auto">Write my resume</Button>{' '}
            </div>

            <figure className="write-resume__img" data-aos="fade-in">
                <img src={`${imageUrl}desktop/write-resume-bg.png`} className="bdr-radius" alt="Not getting enough calls from recruiters ?" />
                <span className="resume-tween1" data-aos="fade-up" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                    <img src={`${imageUrl}desktop/resume-tween1.png`} alt="resume writing service banner 1" />
                </span>
                <span className="resume-tween2" data-aos="fade-right" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200" data-aos-duration="1000">
                    <img src={`${imageUrl}desktop/resume-tween2.svg`} alt="resume writing service banner 2" />
                </span>
                <span className="resume-tween3" data-aos="fade-left" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                    <img src={`${imageUrl}desktop/resume-tween3.svg`} alt="resume writing service banner 3" />
                </span>
            </figure>
        </section>
    )
}

export default WriteMyResume;