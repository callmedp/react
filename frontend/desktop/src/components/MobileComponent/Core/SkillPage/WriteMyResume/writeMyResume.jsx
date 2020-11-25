import React from 'react';
import { Link } from 'react-router-dom';
import './writeMyresume.scss';

const WriteMyResume = (props) => {
    return (
        <section className="m-container mt-0 mb-0">
            <div className="m-write-resume">
                <div className="m-write-resume__text">
                    <strong className="m-heading3">Not getting enough calls from recruiters ?</strong>
                    <p>Make your resume stand out by letting our experts write it for you</p>
                    <Link className="btn-blue-outline" to={"#"}>Write my resume</Link>
                </div>
                <figure className="m-write-resume__img">
                    <img src="./media/images/mobile/write-resume.png" alt="Not getting enough calls from recruiters ?" />
                </figure>
            </div>
        </section>
    )
}

export default WriteMyResume;