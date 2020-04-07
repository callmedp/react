import React from 'react';
import './banner.scss'

export default function Banner(){
    return (

        <div className="banner">
            <div className="container-box">
                <h1 className="mb-20"><span>Smart <br/>Resume Score Checker</span></h1>
                <p className="fs-16">Get the <strong>free review</strong> <br/>of your resume in <br/><strong>just 30 sec</strong></p>
                
                <div className="banner__image">
                    <img src="/media/images/banner-image.png" alt=""/>
                    <div className="circle"></div>
                    <div className="dots"></div>
                </div>
            </div>
        </div>
        );
    }