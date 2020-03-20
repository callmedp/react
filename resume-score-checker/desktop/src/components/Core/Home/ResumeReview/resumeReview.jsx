import React from 'react';

export default function resumeReview(){
    return (
        <section>
    <div class="container">
        <div class="d-flex justify-content-center">
            <h2><span>Resume detailed review</span></h2>
        </div>

        <div class="resume-detail mt-5">
          <ul class="resume-detail__list">
            <li> 
              <div><i class="sprite green-tick mr-4"></i>Format /Style</div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span>
            </li>
            
            <li>
              <div><i class="sprite green-tick mr-4"></i>Summary & Objective</div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span>
            </li>

            <li class="active">
              <div><i class="sprite question-mark mr-4"></i>Accomplishments</div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span>
            </li>
            
            <li>
              <div><i class="sprite green-tick mr-4"></i>Education Details </div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span>
            </li>

            <li>
              <div><i class="sprite caution-mark mr-4"></i>Skills </div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span></li>
            <li>

              <div><i class="sprite green-tick mr-4"></i>Work Experience </div>
              <span class="fs-12"><strong class="fs-16">70</strong>/100</span>
            </li>
            <li>

              <div>
                <i class="sprite green-tick mr-4"></i>Contact Details </div>
                <span class="fs-12"><strong class="fs-16">70</strong>/100</span></li>
          </ul>

          <div class="resume-detail__contentWrap">
            <div class="resume-detail__content">
              <div class="resume-detail__content--head">
                <h3>Resume Format/ Style score</h3>
                <div class="resume-detail__content--progressBar">
                  <div class="sm-progress-circle" data-progress="70">
                    <div class="sm-progress-circle__text">
                      <strong>70</strong>
                    </div>
                    <div class="ko-circle">
                        <div class="full sm-progress-circle__slice">
                            <div class="sm-progress-circle__fill"></div>
                        </div>
                        <div class="sm-progress-circle__slice">
                            <div class="sm-progress-circle__fill"></div>
                            <div class="sm-progress-circle__fill sm-progress-circle__bar"></div>
                        </div>
                    </div>
                    <div class="sm-progress-circle__overlay"></div>
                </div>
                </div>
              </div>
              <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

              <ul class="mt-5">
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                <li>When an unknown printer took a galley of type and scrambled it to make a type.</li>
                <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="mark-info">
          <span class="mr-5"><i class="sprite green-tick mr-3"></i>Available in resume</span>
          <span class="mr-5"><i class="sprite question-mark mr-3"></i>Missing in resume</span>
          <span><i class="sprite caution-mark mr-3"></i>Need major attention</span>
        </div>
    </div>
</section>    
    );
}