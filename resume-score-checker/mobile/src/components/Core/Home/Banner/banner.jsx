import React from 'react';
import { Link } from 'react-router-dom';
import './banner.scss';
import { imageUrl } from '../../../../Utils/domains';

export default function Banner(){
    return (

        <div className="banner">
            <div className="container-box">
                <h1 className="mb-20"><span>Smart <br/>Resume Score Checker</span></h1>
                <p className="fs-16">Get the <strong>free review</strong> <br/>of your resume in <br/><strong>just 30 sec</strong></p>
                {
                    localStorage.getItem('resume_score') ? 
                    (<Link to="/resume-score-checker/score-checker" className="btn btn-md btn-outline-white btn-round-30 mt-5 d-inline-block">
                        Check Score
                    </Link>):null
                }
                
                <div className="banner__image">
                    <img src={`${imageUrl}score-checker/images/mobile/banner-image.png`} alt="Banner"/>
                    <div className="circle"></div>
                    <div className="dots"></div>
                </div>
            </div>
        </div>
        );
    }