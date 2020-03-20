import React from 'react';

export default function ImproveScore(){
    return (

<section class="improve-score">
    <div class="container">
      <div class="improve-score__wrap">
        <div class="improve-score__leftPan">
          <h2><span>Time to improve your resume score</span></h2>
          <p>“Figuring out the way to improve your resume score?” Reach out to our professional resume writers to make your resume more compelling.</p>
        </div>
    
        <div class="improve-score__rightPan">
          <span class="circle"></span>
          <div class="improve-score__rightPan__items">
            <p class="text-right"><img src="{% static 'shinelearn/images/score-checker/resume-writing.png' %}" alt=""/></p>
            <p>Perfect your <br/>resume score with <a href="#">Resume Writing Service</a></p>
            <a href="#" class="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Get details</a>
          </div>
          
          <div class="improve-score__rightPan__items">
            <p class="text-right"><img src="{% static 'shinelearn/images/score-checker/resume-builder.png' %}" alt=""/></p>
            <p>Create a <br />Perfect Resume with <a href="#">Resume Builder</a></p>
            <a href="#" class="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Create now</a>
          </div>
  
          <div class="improve-score__rightPan__items d-lg-none d-xl-block">
            <p class="text-right"><img src="{% static 'shinelearn/images/score-checker/free-resume-format.png' %}" alt=""/></p>
            <p>Explore <br /><a href="#">Free resume Formats</a><br />to search desired jobs</p>
            <a href="#" class="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Explore now</a>
          </div>
          <span class="dots"></span>
        </div>
      </div>
    </div>
  </section>
    );
}