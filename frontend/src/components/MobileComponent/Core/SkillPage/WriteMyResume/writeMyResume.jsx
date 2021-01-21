import React from 'react';
import './writeMyresume.scss';
import { Button } from 'react-bootstrap';
import { resumeShineSiteDomain, imageUrl } from 'utils/domains';


const WriteMyResume = (props) => {
    const builderRedirect = () => window.location.href = `${resumeShineSiteDomain}`;

    return (
        <section className="m-container mt-0 mb-0" data-aos="fade-up">
            <div className="m-write-resume d-flex">
                <div className="m-write-resume__text">
                    <strong className="m-heading3">Not getting enough calls from recruiters ?</strong>
                    <p>Make your resume stand out by letting our experts write it for you</p>
                    <Button className="btn-blue-outline" onClick={builderRedirect}>Write my resume</Button>
                </div>
                <figure className="m-write-resume__img">
                    <img src={`${imageUrl}mobile/write-resume.png`} alt="Not getting enough calls from recruiters ?" />
                </figure>
            </div>
        </section>
    )
}

export default WriteMyResume;