import React from 'react';

export default function Banner(){
    return (
<section class="banner">
    <div class="container h-100">
        <div class="row h-100">
            <div class="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                <h1>
                    <span>Smart Resume Score Checker</span>
                </h1>
                <p class="">Get the <strong>free review</strong> of your resume in <strong>just 30 sec</strong></p>

                <div class="d-flex mt-5">
                    <div class="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        <i class="sprite upload mr-3"></i> Upload resume                                
                        <input class="file-upload__input" type="file" name="file"/>
                    </div>

                    <a href="#" class="d-flex align-items-center btn btn-outline-light btn-round-40 font-weight-bold px-4">
                        <i class="sprite export mr-3"></i>
                        Export from shine.com
                    </a>
                </div>
                <p class="banner__text">PDF, DOC, DOCX only  |  Max file size: 5MB</p>
            </div>
            <div class="col-md-6">
                <div class="banner__image">
                    <img aria-label="header image" class="banner__image" src="{% static 'shinelearn/images/score-checker/banner-img.png' %}"/>
                </div>
            </div>
        </div>
    </div>
</section>
    );
}