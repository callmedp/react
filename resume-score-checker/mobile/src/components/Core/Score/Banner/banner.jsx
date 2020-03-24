import React from 'react';

export default function Banner() {
    return(
        <div>
            <div className="score-banner">
            <div className="container-box">
                <h1 className="mb-10"><span>Hello Sachin <br/>Your resume scored 70 out of 100</span></h1>
                
                <div className="score-banner__image">
                    <div class="score-banner__progressBar">
                        <div class="ko-progress-circle" data-progress="70">
                        <div class="ko-progress-circle__text">
                            <strong>70</strong>
                            <p class="fs-12">Resume score</p>
                        </div>
                        <div class="ko-circle">
                            <div class="full ko-progress-circle__slice">
                                <div class="ko-progress-circle__fill"></div>
                            </div>
                            <div class="ko-progress-circle__slice">
                                <div class="ko-progress-circle__fill"></div>
                                <div class="ko-progress-circle__fill ko-progress-circle__bar"></div>
                            </div>
                        </div>
                        <div class="ko-progress-circle__overlay"></div>
                        </div>
                    </div>
                </div>
                <div class="circle"></div>
                <div class="dots"></div>                
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