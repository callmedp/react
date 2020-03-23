import React from 'react';

export default function ResumeReview(){
    return (
        <section>
    <div className="container">
        <div className="d-flex justify-content-center">
            <h2><span>Resume detailed review</span></h2>
        </div>

        <div className="resume-detail mt-5">
          <ul className="resume-detail__list">
            <li> 
              <div><i className="sprite green-tick mr-4"></i>Format /Style</div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span>
            </li>
            
            <li>
              <div><i className="sprite green-tick mr-4"></i>Summary & Objective</div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span>
            </li>

            <li className="active">
              <div><i className="sprite question-mark mr-4"></i>Accomplishments</div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span>
            </li>
            
            <li>
              <div><i className="sprite green-tick mr-4"></i>Education Details </div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span>
            </li>

            <li>
              <div><i className="sprite caution-mark mr-4"></i>Skills </div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span></li>
            <li>

              <div><i className="sprite green-tick mr-4"></i>Work Experience </div>
              <span className="fs-12"><strong className="fs-16">70</strong>/100</span>
            </li>
            <li>

              <div>
                <i className="sprite green-tick mr-4"></i>Contact Details </div>
                <span className="fs-12"><strong className="fs-16">70</strong>/100</span></li>
          </ul>

          <div className="resume-detail__contentWrap">
            <div className="resume-detail__content">
              <div className="resume-detail__content--head">
                <h3>Resume Format/ Style score</h3>
                <div className="resume-detail__content--progressBar">
                  <div className="sm-progress-circle" data-progress="70">
                    <div className="sm-progress-circle__text">
                      <strong>70</strong>
                    </div>
                    <div className="ko-circle">
                        <div className="full sm-progress-circle__slice">
                            <div className="sm-progress-circle__fill"></div>
                        </div>
                        <div className="sm-progress-circle__slice">
                            <div className="sm-progress-circle__fill"></div>
                            <div className="sm-progress-circle__fill sm-progress-circle__bar"></div>
                        </div>
                    </div>
                    <div className="sm-progress-circle__overlay"></div>
                </div>
                </div>
              </div>
              <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

              <ul className="mt-5">
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                <li>When an unknown printer took a galley of type and scrambled it to make a type.</li>
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="mark-info">
          <span className="mr-5"><i className="sprite green-tick mr-3"></i>Available in resume</span>
          <span className="mr-5"><i className="sprite question-mark mr-3"></i>Missing in resume</span>
          <span><i className="sprite caution-mark mr-3"></i>Need major attention</span>
        </div>
    </div>
</section>    
    );
}