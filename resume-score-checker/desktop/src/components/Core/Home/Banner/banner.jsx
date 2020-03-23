import React from 'react';
import './banner.scss'

export default function Banner(){
    return (
<section className="banner">
    <div className="container h-100">
        <div className="row h-100">
            <div className="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                <h1>
                    <span>Smart Resume Score Checker</span>
                </h1>
                <p className="">Get the <strong>free review</strong> of your resume in <strong>just 30 sec</strong></p>

                <div className="d-flex mt-5">
                    <div className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        <i className="sprite upload mr-3"></i> Upload resume                                
                        <input className="file-upload__input" type="file" name="file"/>
                    </div>

                    <a href="#" className="d-flex align-items-center btn btn-outline-light btn-round-40 font-weight-bold px-4">
                        <i className="sprite export mr-3"></i>
                        Export from shine.com
                    </a>
                </div>
                <p className="banner__text">PDF, DOC, DOCX only  |  Max file size: 5MB</p>
            </div>
            <div className="col-md-6">
                <div className="banner__image">
                    <img aria-label="header image" className="banner__image" src="media/images/banner-img.png"/>
                </div>
            </div>
        </div>
    </div>
</section>
    );
}