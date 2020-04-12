import React from 'react';
import './improveScore.scss'
const ImproveScore=props=> {
  return (

    <section className="improve-score">
      <div className="container">
        <div className="improve-score__wrap">
          <div className="improve-score__leftPan">
            <h2><span>Time to improve your resume score</span></h2>
            <p>“Figuring out the way to improve your resume score?” Reach out to our professional resume writers to make your resume more compelling.</p>
          </div>

          <div className="improve-score__rightPan">
            <span className="circle"></span>
            <div className="improve-score__rightPan__items">
              <p className="text-right"><img src={"media/images/resume-writing.png"} alt="" /></p>
              <p>Perfect your <br />resume score with <a href="https://learning.shine.com/services/resume-services/mid-level/pd-1923">Resume Writing Service</a></p>
              <a href="https://learning.shine.com/services/resume-services/mid-level/pd-1923" className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Get details</a>
            </div>

            <div className="improve-score__rightPan__items">
              <p className="text-right"><img src={"media/images/resume-builder.png"} alt="" /></p>
              <p>Create a <br />Perfect Resume with <a href="https://learning.shine.com/resume-builder/">Resume Builder</a></p>
              <a href="https://learning.shine.com/resume-builder/" className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Create now</a>
            </div>

            <div className="improve-score__rightPan__items d-lg-none d-xl-block">
              <p className="text-right"><img src={"media/images/free-resume-format.png"} alt="" /></p>
              <p>Explore <br /><a href="https://learning.shine.com/cms/resume-format/1/">Free resume Formats</a><br />to search desired jobs</p>
              <a href="https://learning.shine.com/cms/resume-format/1/" className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Explore now</a>
            </div>
            <span className="dots"></span>
          </div>
        </div>
      </div>
    </section>
  );
}

export default  ImproveScore;