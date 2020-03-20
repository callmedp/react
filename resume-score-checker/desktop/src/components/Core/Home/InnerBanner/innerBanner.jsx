import React from 'react';


export default function InnerBanner(){
    return (
<div>        
<section class="banner">
    <div class="container h-100">
        <div class="row h-100">
            <div class="col-md-6">
                <div class="banner-score">
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                          <li class="breadcrumb-item"><a href="#">Home</a></li>
                          <li class="breadcrumb-item active" aria-current="page">Library</li>
                        </ol>
                    </nav>

                    <div class="banner-score__resume-scoreWrap">
                      <div class="banner-score__progressBar">

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
                      
                      <div class="banner-score__myresume">
                        <a href="#">
                          <i class="sprite clip"></i>
                          Myresume.doc
                        </a>

                        <a href="#" class="btn btn-outline-primary btn-round-40 fs-12 py-1">Download</a>
                      </div>
                    </div>

                </div>
            </div>
            <div class="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                <h1 class="fs-30">
                    <span>Hello Sachin,<br/>Your resume Scored 70 out of 100</span>
                </h1>
                <p class="text-white-50">Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile</p>

                <div class="d-flex mt-5">
                    <a href="#" class="btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        Get expert help
                    </a>

                    <div class="file-upload btn btn-outline-light btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        <i class="sprite export mr-3"></i> Upload new resume                                
                        <input class="file-upload__input" type="file" name="file"/>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</section>
<section class="howItWork" style={{height: '50px'}}></section>
</div>
    );
}