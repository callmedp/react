import React from 'react';
import './howItWorks.scss'

export default function HowItWorks(){
    return (
        
<section className="container resume-checker my-0">
    <div className="row">
        <div className="col-md-5 pr-5">
            <h2>
                <span>How Resume Checker Works?</span>
            </h2>
            <p className="fs-15">When you upload your resume, our AI-powered system analyzes it against key criteria required as per the Industry standards and commit an overall score to your resume. Our resume checker it gives you the fair idea of the resume quality and how it represents you in front of recruiters & hiring manager.  We also provide you a detailed resume review and ways to increase the score further. You can also reach out to our professional resume experts to perfect your resume score.</p>
        </div>
        <div className="col-md-7 pl-4">
            <ul className="resume-checker__steps">
                <li className="resume-checker__step">
                    <span className="resume-checker__stepCircle mr-3"><i className="sprite upload-resume d-block"></i></span>
                    <div className="resume-checker__content">
                        <p className="resume-checker__content--heading mb-0 font-weight-bold">Upload Resume</p>
                        <p>Just upload your resume or export it from shine.com</p>
                    </div>
                </li>
                <li className="resume-checker__step">
                    <span className="resume-checker__stepCircle mr-3"><i className="sprite resume-analysis d-block"></i></span>
                    <div className="resume-checker__content">
                        <p className="resume-checker__content--heading mb-0 font-weight-bold">Resume Analysis</p>
                        <p>Style and content of resume will be checked by industry experts</p>
                    </div>
                </li>
                <li className="resume-checker__step">
                    <span className="resume-checker__stepCircle mr-3"><i className="sprite get-resume d-block"></i></span>
                    <div className="resume-checker__content"
                    >
                        <p className="resume-checker__content--heading mb-0 font-weight-bold">Get Report in 30 sec</p>
                        <p>After checking your resume you will get your resume score also will let you know how to get it improved</p>
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <div className="text-center mt-5"><a href="#" className="btn btn-primary btn-round-40 px-5 py-4 mr-5">Check the score now</a></div>
</section>
    );
}