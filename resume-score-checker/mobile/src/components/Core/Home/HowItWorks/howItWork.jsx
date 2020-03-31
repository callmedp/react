import React, {Component} from 'react';

class HowItWorks extends Component {
    render() {
        return(
            <div className="container-box">
                <h2 className="mb-15"><span>How Does Resume Checker Works?</span></h2>
                
                <p>When you upload your resume, our system analyzes it against key criteria required per the industry standards and assigns an overall score to your resume which gives you the fair idea of its quality and how it represents you in front of the recruiters and the hiring manager. We also provide you a detailed review and ways to improve the score further. You could also reach out to our professional resume experts to perfect the score.</p>
    
                <ul className="resume-checker__steps">
                    <li className="resume-checker__step">
                        <span className="resume-checker__stepCircle mr-3">
                            <i className="sprite upload-resume d-block"></i>
                        </span>
                        <div className="resume-checker__content">
                            <p className="resume-checker__content--heading mb-0 font-weight-bold">Upload Resume</p>
                            <p>Just upload your resume or export it from shine.com</p>
                        </div>
                    </li>
                    <li className="resume-checker__step">
                        <span className="resume-checker__stepCircle mr-3">
                            <i className="sprite resume-analysis d-block"></i>
                        </span>
                        <div className="resume-checker__content">
                            <p className="resume-checker__content--heading mb-0 font-weight-bold">Resume Analysis</p>
                            <p>Style and content of resume will be checked by industry experts</p>
                        </div>
                    </li>
                    <li className="resume-checker__step">
                        <span className="resume-checker__stepCircle mr-3">
                            <i className="sprite get-resume d-block"></i>
                        </span>
                        <div className="resume-checker__content"
                        >
                            <p className="resume-checker__content--heading mb-0 font-weight-bold">Get Report in 30 sec</p>
                            <p>After checking your resume you will get your resume score also will let you know how to get it improved</p>
                        </div>
                    </li>
                </ul>
            </div>
        );
    }
}

export default HowItWorks;