import React from 'react';

export default function Benefits() {
    return (
        <section class="container">
            <div class="row benefits">
                <div class="col-md-6 benefits__left">
                    <h2><span>What's next- Benefits after getting resume score</span></h2>
                    <p>For a small fee, our professional resume writers can help you take those tips and make your resume, cover letter, and even LinkedIn profile into exactly what recruiters are looking for.</p>
                    <a href="#" class="btn btn-primary btn-round-40 px-5 py-4 mr-5 mt-5">Check the score now</a>
                </div>
                <div class="col-md-6 pl-5 justify-content-end">
                    <div class="benefits__listBox">
                        <ul class="benefits__lists">
                            <li class="benefits__item">One-on-one support from a professional writer.</li>
                            <li class="benefits__item">Get resume services & increase your resume views</li>
                            <li class="benefits__item">Optimize your job search funnel</li>
                            <li class="benefits__item">Rich in keywords to set you up with the desired jobs</li>
                        </ul>
                    </div>

                    <span class="circle"></span>
                    <span class="dots"></span>
                    <span class="benefits__men"></span>
                </div>
            </div>
        </section>
    );
}