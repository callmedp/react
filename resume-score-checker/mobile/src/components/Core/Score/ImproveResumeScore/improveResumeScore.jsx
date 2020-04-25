import React from 'react';
import { imageUrl, siteDomain } from '../../../../Utils/domains';
import { eventClicked } from '../../../../stores/googleAnalytics/actions/index';
import { useDispatch } from 'react-redux';
import './improveResumeScore.scss';

export default function ImproveResumeScore() {

    const dispatch = useDispatch();
    const handleEventClick =(action,label) =>{
        dispatch(eventClicked({
            'action': action,
            'label': label
        }))
    }

    return (
        <div className="improve-resume pb-30">
            <div className="container-box">
                <h2><span>Time to improve your resume score</span></h2>
                <p className="mt-15">Stuck on how to perfect your resume score? Reach out to our professional resume writers to get expert assistance</p>
            </div>

            <div className="improve-resume__slider">
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/mobile/resume-writing.png`} alt="resume-writing"/>
                    </span>
                    <p className="improve-resume__head mb-20">Perfect your resume score with <strong>Resume Writing Service</strong></p>
                    <a href = {`${siteDomain}/services/resume-writing/63/`} className="btn btn-round-30 btn-outline-blue px-15" onClick={()=>handleEventClick('M_Resumewriting','Improvescore')}>Get details</a>
                </div>
                
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/mobile/resume-builder.png`} alt="resume-builder"/>
                    </span>
                    <p className="improve-resume__head mb-20">Create a Perfect Resume with <strong>Resume Builder</strong></p>
                    <a href={`${siteDomain}/resume-builder/`} className="btn btn-round-30 btn-outline-blue px-15" onClick={()=>handleEventClick('M_ResumeBuilder','Improvescore')}>Create Now</a>
                </div>
                
                <div className="improve-resume__slide">
                    <span className="improve-resume__image">
                        <img src={`${imageUrl}score-checker/images/mobile/free-resume-format.png`} alt="resume-format"/>
                    </span>
                    <p className="improve-resume__head mb-20">Explore <strong>Free resume Formats</strong>to search desired jobs</p>
                    <a href={`${siteDomain}/cms/resume-format/1/`} className="btn btn-round-30 btn-outline-blue px-15" onClick={()=>handleEventClick('M_ResumeFormat','Improvescore')}>Explore Now</a>
                </div>
            </div>
        </div>
    );
}