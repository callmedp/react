import React from 'react';


export default function InnerBanner(){
    return (
<div>        
<section className="banner">
    <div className="container h-100">
        <div className="row h-100">
            <div className="col-md-6">
                <div className="banner-score">
                    <nav aria-label="breadcrumb">
                        <ol className="breadcrumb">
                          <li className="breadcrumb-item"><a href="#">Home</a></li>
                          <li className="breadcrumb-item active" aria-current="page">Library</li>
                        </ol>
                    </nav>

                    <div className="banner-score__resume-scoreWrap">
                      <div className="banner-score__progressBar">

                        <div className="ko-progress-circle" data-progress="70">
                          <div className="ko-progress-circle__text">
                            <strong>70</strong>
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
                      
                      <div className="banner-score__myresume">
                        <a href="#">
                          <i className="sprite clip"></i>
                          Myresume.doc
                        </a>

                        <a href="#" className="btn btn-outline-primary btn-round-40 fs-12 py-1">Download</a>
                      </div>
                    </div>

                </div>
            </div>
            <div className="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                <h1 className="fs-30">
                    <span>Hello Sachin,<br/>Your resume Scored 70 out of 100</span>
                </h1>
                <p className="text-white-50">Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile</p>

                <div className="d-flex mt-5">
                    <a href="#" className="btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        Get expert help
                    </a>

                    <div className="file-upload btn btn-outline-light btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        <i className="sprite export mr-3"></i> Upload new resume                                
                        <input className="file-upload__input" type="file" name="file"/>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</section>
<section className="howItWork" style={{height: '50px'}}></section>
</div>
    );
}