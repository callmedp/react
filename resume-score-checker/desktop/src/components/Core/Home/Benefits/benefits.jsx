import React from 'react';
import './benefits.scss'

export default function Benefits() {
    return (
        <section className="container">
            <div className="row benefits">
                <div className="col-md-6 benefits__left">
                    <h2><span>What's next- Benefits after getting resume score</span></h2>
                    <p>For a small fee, our professional resume writers can help you take those tips and make your resume, cover letter, and even LinkedIn profile into exactly what recruiters are looking for.</p>
                    <a href="#" className="btn btn-primary btn-round-40 px-5 py-4 mr-5 mt-5">Check the score now</a>
                </div>
                <div className="col-md-6 pl-5 justify-content-end">
                    <div className="benefits__listBox">
                        <ul className="benefits__lists">
                            <li className="benefits__item">One-on-one support from a professional writer.</li>
                            <li className="benefits__item">Get resume services & increase your resume views</li>
                            <li className="benefits__item">Optimize your job search funnel</li>
                            <li className="benefits__item">Rich in keywords to set you up with the desired jobs</li>
                        </ul>
                    </div>

                    <span className="circle"></span>
                    <span className="dots"></span>
                    <span className="benefits__men"></span>
                </div>
            </div>
        </section>
    );
}