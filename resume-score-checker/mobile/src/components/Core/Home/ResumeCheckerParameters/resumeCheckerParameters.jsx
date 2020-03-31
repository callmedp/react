import React, {Component} from 'react';

class Parameters extends Component {
    render() {
        return(
            <section className="parameters pb-10">
            <div className="container-box">
                <div className="d-flex">
                    <h2><span>Resume checker <br/>Parameters</span></h2>
                </div>
        
                <div className="media align-items-center">
                  <ul className="parameters__lists mt-5">
                      <li className="parameters__item">
                          <p className="parameters__head">Format /Style</p>
                          <p>It checks font size, font family, resume structure flow, sections and length of the resume.</p>
                      </li>
      
                      <li className="parameters__item">
                          <p className="parameters__head">Education Details</p>
                          <p>It evaluates all the required educational details such as your latest qualifications, year of graduation, overall marks scored etc.</p>
                      </li>
      
                      <li className="parameters__item">
                          <p className="parameters__head">Summary &amp; Objective</p>
                          <p>This resume section communicates your overall work experience and expectations to the recruiters at one go.</p>
                      </li>
      
                      <li className="parameters__item">
                          <p className="parameters__head">Skills &amp; Work Experience</p>
                          <p>It makes sure you have skills and work experience in your resume based on job opportunities you’re looking for.</p>
                      </li>
                      
                      <li className="parameters__item">
                          <p className="parameters__head">Contact Details</p>
                          <p>It checks the presence of name, email-id, address and mobile number, LinkedIn profile in resume. </p>
                      </li>
                      <li className="parameters__item">
                          <p className="parameters__head">Resume action verbs</p>
                          <p>Resume checker validates and makes sure you’ve used strong action verbs as well as other index of a strong impact- oriented resume.</p>
                      </li>
                  </ul>
                </div>
            </div>
          </section>
        );
    }
}

export default Parameters;