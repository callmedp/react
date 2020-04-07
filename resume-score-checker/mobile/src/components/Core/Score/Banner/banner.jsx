import React from 'react';
import { useSelector } from 'react-redux';
import './score-banner.scss';

export default function Banner() {
    const localValue = JSON.parse(localStorage.getItem('resume_score'))
    const storeValue = useSelector(state => state.uploadFile.score)

    const score = localStorage.getItem('resume_score') === null ? storeValue : localValue.score
    return(
        <div>
            <div className="score-banner">
            <div className="container-box">
                <h1 className="mb-10"><span>Hello Sachin <br/>Your resume scored {score} out of 100</span></h1>
                
                <div className="score-banner__image">
                    <div className="score-banner__progressBar">
                        <div className="ko-progress-circle" data-progress={score}>
                        <div className="ko-progress-circle__text">
                            <strong>{score}</strong>
                            <p className="fs-12">Resume score</p>
                        </div>
                        <div className="ko-circle">
                            <div className="full ko-progress-circle__slice">
                                <div className="ko-progress-circle__fill"></div>
                            </div>
                            <div className="ko-progress-circle__slice">
                                <div className="ko-progress-circle__fill"></div>
                                <div className="ko-progress-circle__fill ko-progress-circle__bar"></div>
                            </div>
                        </div>
                        <div className="ko-progress-circle__overlay"></div>
                        </div>
                    </div>
                </div>
                <div className="circle"></div>
                <div className="dots"></div>                
            </div>
        </div>

            <div className="container-box">
                <div className="resume-detail mb-30 text-center">
                    <p>
                        <a href="#">
                            <i className="sprite clip"></i>
                            Myresume.doc
                        </a>
                    </p>
                    {/* <a href="#" className="btn btn-round-30 btn-outline-blue py-5">Download</a> */}
                    <p className="mt-15">Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile</p>
                </div>
               
            </div>
        </div>
        
    );
} 