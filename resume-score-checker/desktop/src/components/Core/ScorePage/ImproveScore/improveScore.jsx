import React from 'react';
import './improveScore.scss'
import { siteDomain } from '../../../../utils/domains';
const ImproveScore = props => {
  const staticUrl = window&& window.config && window.config.staticUrl || '/media/static/'
  return (

    <section className="improve-score">
      <div className="container">
        <div className="improve-score__wrap">
          <div className="improve-score__leftPan">
            <h2><span>Time to improve your resume score</span></h2>
            <p>Stuck on how to perfect your resume score? Reach out to our professional resume writers to get expert assistance</p>
          </div>

          <div className="improve-score__rightPan">
            <span className="circle"></span>
            <div className="improve-score__rightPan__items">
              <p className="text-right"><img src={`${staticUrl}score-checker/images/resume-writing.png`} alt="resume writing" /></p>
              <p>Perfect your <br />resume score with <a href={`${siteDomain}/services/resume-writing/63/`}>Resume Writing Service</a></p>
              <a href={`${siteDomain}/services/resume-writing/63/`} className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Get details</a>
            </div>

            <div className="improve-score__rightPan__items">
              <p className="text-right"><img src={`${staticUrl}score-checker/images/resume-builder.png`} alt="" /></p>
              <p>Create a <br />Perfect Resume with <a href={`${siteDomain}/resume-builder/`}>Resume Builder</a></p>
              <a href={`${siteDomain}/resume-builder/`} className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Create now</a>
            </div>

            <div className="improve-score__rightPan__items d-lg-none d-xl-block">
              <p className="text-right"><img src={`${staticUrl}score-checker/images/free-resume-format.png`} alt="" /></p>
              <p>Explore <br /><a href={`${siteDomain}/cms/resume-format/1/`} >Free resume Formats</a><br />to search desired jobs</p>
              <a href={`${siteDomain}/cms/resume-format/1/`} className="btn btn-round-40 btn-outline-primary px-5 py-4 my-3">Explore now</a>
            </div>
            <span className="dots"></span>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ImproveScore;