import React from 'react';
import Button from 'react-bootstrap/Button';
import './writeMyresume.scss';

const WriteMyResume = (props) => {
    return (
        <section className="write-resume">
            <div className="write-resume__text">
                <strong className="heading3">Not getting enough calls from recruiters ?</strong>
                <p>Make your resume stand out by letting our experts write it for you</p>
                <Button variant="outline-primary" className="ml-auto">Write my resume</Button>{' '}
            </div>
            <figure className="write-resume__img">
                <img src="./media/images/write-resume.png" alt="Not getting enough calls from recruiters ?" />
            </figure>
        </section>
    )
}

export default WriteMyResume;