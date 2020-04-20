import React from 'react';
import { imageUrl } from '../../../../Utils/domains';

export default function ImproveResumeScore() {
    return (
        <div className="improve-resume pb-30">
            <div className="container-box">
                <h2><span>Time to improve your resume score</span></h2>
                <p className="mt-15">Stuck on how to perfect your resume score? Reach out to our professional resume writers to get expert assistance</p>
            </div>

            <div className="improve-resume__slider">
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/resume-writing.png`} alt="resume-writing"/>
                    </span>
                    <p className="improve-resume__head mb-20">Perfect your resume score with <strong>Resume Writing Service</strong></p>
                    <a href="https://learning.shine.com/services/resume-writing/63/" className="btn btn-round-30 btn-outline-blue px-15">Get details</a>
                </div>
                
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/resume-builder.png`} alt="resume-builder"/>
                    </span>
                    <p className="improve-resume__head mb-20">Create a Perfect Resume with <strong>Resume Builder</strong></p>
                    <a href="https://learning.shine.com/resume-builder/" className="btn btn-round-30 btn-outline-blue px-15">Create Now</a>
                </div>
                
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/free-resume-format.png`} alt="resume-format"/>
                    </span>
                    <p className="improve-resume__head mb-20">Explore <strong>Free resume Formats</strong>to search desired jobs</p>
                    <a href="https://learning.shine.com/cms/resume-format/1/" className="btn btn-round-30 btn-outline-blue px-15">Explore Now</a>
                </div>
            </div>
        </div>
    );
}